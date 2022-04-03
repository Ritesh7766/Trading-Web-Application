from flask import Flask, render_template, url_for, flash, redirect
from include.forms import LoginForm, RegistrationForm
from include import app


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account successfully created for {form.username.data}', category = 'success')
        return redirect(url_for('index'))
    elif form.errors != {}:
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error creating user: {err_msg}', category = 'danger')
    return render_template('register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'hello' and form.password.data == 'hello':
            flash('Success', category = 'success')
        else:
            flash('Failure', category = 'danger')
    return render_template('login.html', form = form)
