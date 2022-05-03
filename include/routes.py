from flask import Flask, render_template, url_for, flash, redirect, jsonify, request, session
from include.forms import LoginForm, RegistrationForm, PurchaseForm
from include.models import User, Stock, Stocks_Owned, Transaction
from include import app, db
from flask_login import login_user, current_user, logout_user
from include.utils import logout_required, login_required, lookup_symbol
from datetime import datetime


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/register', methods = ['GET', 'POST'])
@logout_required(current_user, redirect)
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create a new instance of the user.
        user = User(username = form.username.data, email = form.email.data, password = form.password.data)

        # Add the user to the database.
        db.session.add(user)
        db.session.commit()

        # SQL equivalent:
        # INSERT INTO user (username, email, password) VALUES (form.username, form.email, password_hash)
        
        # Let the user know that the account has been created.
        flash(f'Account successfully created for {form.username.data}', category = 'success')
        
        # Redirect to the login page.
        return redirect(url_for('login'))

    elif form.errors != {}:
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error creating user: {err_msg}', category = 'danger')

    return render_template('register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
@logout_required(current_user, redirect)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Find a user with the given credentials
        user = User.query.filter_by(email = form.email.data).first()

        # If credentials are correct, than log in the user.
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful.', category = 'success')
            return redirect(url_for('index'))
        else: 
            flash('Login unsuccessful. Please check email and password.', category = 'danger')
    return render_template('login.html', form = form)


@app.route('/logout')
@login_required(current_user, redirect)
def logout():
    logout_user()
    flash('You were logged out of your account.', category = 'primary')
    return redirect(url_for('index'))


@app.route('/availableStocks')
@login_required(current_user, redirect)
def available_stocks():
    return render_template('available_stocks.html')


@app.route('/quote', methods = ['GET', 'POST'])
@login_required(current_user, redirect)
def quote():
    # Default views for users.
    views = ['Overview', 'Fundamentals', 'News']
    # If user has entered a symbol.      
    if request.method == 'POST' or request.args.get('sym'):
        symbol = request.form.get('symbol') if request.method == 'POST' else request.args.get('sym')
        view = request.form.get('view')
        if not view: view = 'Overview'
        symbol = symbol.upper()
        # Validate view
        if view not in views:
            flash('Invalid input.', category = 'warning')
            return redirect('quote')
        # If symbol already exits in the session variable, than there is no need to make an api call.
        if symbol in session:
            stock_info = session[symbol]
        # Otherwise make an api call.
        else: stock_info = lookup_symbol(symbol)
        if not stock_info:
            flash('Invalid symbol.', category = 'warning')
        else:
            # If the symbol is correct make sure it exists in our database.
            res = db.engine.execute(f'SELECT symbol FROM stock WHERE symbol = "{symbol}"')
            if not res:
                new_stock = Stock(symbol = symbol, company_name = stock_info[symbol]['company']["companyName"])
                db.session.add(new_stock)
                db.session.commit()
            # Add info to the session variable.
            session[symbol] = stock_info
            return render_template('quoted.html', stock_info = stock_info[symbol], view = view, views = views, datetime=datetime)
    return render_template('quote.html', views = views)


@app.route('/view')
@login_required(current_user, redirect)
def view():
    sym = request.args.get('sym')
    if sym not in session:
        return None
    return jsonify(session[sym][sym])


@app.route('/search')
@login_required(current_user, redirect)
def search():
    sym = request.args.get('sym')
    nm = request.args.get('nm')
    data, res = [], None
    # If user has entered a symbol, than search by symbol.
    if sym:
        res = db.engine.execute(f'SELECT * FROM stock WHERE stock.symbol LIKE "%{sym}%" LIMIT 70')
    # If user has entered a name, than search by name.
    elif nm:
        res = db.engine.execute(f'SELECT * FROM stock WHERE stock.company_name LIKE "%{nm}%" LIMIT 70')
    # If no symbol provided, than return the first 70 stocks.
    if not res:
        res = db.engine.execute(f'SELECT * FROM stock LIMIT 70')
    # Convert the data into a list of dictionaries.
    for symbol, name in res:
        data.append({'symbol': symbol, 'name': name})
    # Return the result in JSON format.
    return jsonify(data)


@app.route('/buy', methods = ['GET', 'POST'])
@login_required(current_user, redirect)
def buy():
    form = PurchaseForm()
    # Make sure symbol exists in session variable.
    symbol = request.args.get('sym')
    if symbol not in session:
        stock_info = lookup_symbol(symbol)
        session[symbol] = stock_info
    stock_info = session[symbol][symbol]
    if form.validate_on_submit():
        if 'submit' not in request.form:
            return redirect(url_for('quote'))
        shares = int(request.form.get('shares'))
        price = float(stock_info['quote']['latestPrice'])
        # Compute the total cost of purchasing the stocks.
        total = shares * price

        # Find the balance of the user.
        balance = current_user.cash
        
        # If the available balance is less than the cost than cancel transaction.
        if balance < total:
            flash(f'Insufficient Balance!', category = 'primary')

        # Otherwise deduct the amount from the current balance.
        current_user.cash -= total
        db.session.commit()

        # Update ownership.
        stock = Stocks_Owned.query.filter_by(user_id = current_user.id, stock_id = stock_info['quote']['symbol']).first()
        # If user already owns this stock than update it.
        if stock:
            stock.shares += shares
        # Otherwise add it to the db
        else:
            stock_owned = Stocks_Owned(user_id = current_user.id, stock_id = stock_info['quote']['symbol'], shares = shares, logo = stock_info['logo']['url'])
            db.session.add(stock_owned)
        db.session.commit()

        # Record the transaction.
        transaction = Transaction(user_id = current_user.id, stock_id = stock_info['quote']['symbol'], shares = shares, price = price)
        db.session.add(transaction)
        db.session.commit()

        flash(f"Purchased {shares} stocks of {stock_info['company']['companyName']} for ${total}", category = 'success')
        return redirect('/')
        
    elif form.errors != {}:
        if 'submit' not in request.form:
            return redirect(url_for('quote'))
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error: {err_msg}', category = 'danger')

    return render_template('buy.html', form = form, stock_info = stock_info)


@app.route('/portfolio')
@login_required(current_user, redirect)
def portfolio():
    # Get all the stocks owned by the user.
    stocks = Stocks_Owned.query.filter_by(user_id = current_user.id).all()
    return render_template('portfolio.html', stocks = stocks)