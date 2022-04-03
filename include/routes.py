from flask import Flask, render_template, url_for, flash, redirect
from include.forms import LoginForm, RegistrationForm
from include.models import User
from include import app, db
from flask_login import login_user, current_user, logout_user


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/register', methods = ['GET', 'POST'])
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
def logout():
    logout_user()
    flash('You were logged out of your account.', category = 'primary')
    return redirect(url_for('index'))