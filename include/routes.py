from flask import Flask, render_template, url_for, flash, redirect, jsonify, request, session
from include.forms import LoginForm, RegistrationForm
from include.models import User, Stock
from include import app, db
from flask_login import login_user, current_user, logout_user
from include.utils import logout_required, login_required, lookup_symbol


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
    views = ['Overview', 'Fundamental']
    # If user has entered a symbol.
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        view = request.form.get('view')
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
            return render_template('quoted.html', stock_info = stock_info[symbol], view = view, views = views)
    return render_template('quote.html', views = views)


@app.route('/search')
@login_required(current_user, redirect)
def search():
    sym = request.args.get('sym')
    nm = request.args.get('nm')
    data, res = [], None
    # If user has entered a symbol, than search by symbol.
    if sym:
        res = db.engine.execute(f'SELECT * FROM stock WHERE stock.symbol LIKE "%{sym}%" LIMIT 20')
    # If user has entered a name, than search by name.
    elif nm:
        res = db.engine.execute(f'SELECT * FROM stock WHERE stock.company_name LIKE "%{nm}%" LIMIT 20')
    # If no symbol provided, than return the first 20 stocks.
    if not res:
        res = db.engine.execute(f'SELECT * FROM stock LIMIT 20')
    # Convert the data into a list of dictionaries.
    for symbol, name in res:
        data.append({'symbol': symbol, 'name': name})
    # Return the result in JSON format.
    return jsonify(data)