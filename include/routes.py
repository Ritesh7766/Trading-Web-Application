from flask import Flask, render_template, url_for, flash, redirect, jsonify, request
from include.forms import LoginForm, RegistrationForm
from include.models import User
from include import app, db
from flask_login import login_user, current_user, logout_user
from include.utils import logout_required, login_required


token = 'Tpk_c1f51c49da9c413a9ea676bfd7322915'
api_url = f'https://sandbox.iexapis.com/stable/stock/IBM/quote?token={token}'


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


@app.route('/quoted')
@login_required(current_user, redirect)
def quoted():
    return render_template('quote.html')


# Limit the number of search results to 20.
@app.route('/quote')
def quote():
    sym = request.args.get('sym')
    nm = request.args.get('nm')
    data, res = [], None
    # If user has entered a symbol, than search by symbol.
    if sym:
        res = db.engine.execute(f'SELECT * FROM stock WHERE stock.symbol LIKE "%{sym}%" LIMIT 20')
    # If user has entered a name, than search by name.
    elif nm:
        res = db.engine.execute(f'SELECT * FROM stock WHERE stock.company_name LIKE "%{nm}%" LIMIT 20')
    # Convert the data into a list of dictionaries.
    if res:
        for symbol, name in res:
            data.append({symbol: name})
    
    # Return the result in JSON format.
    return jsonify(data)