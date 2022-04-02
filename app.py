from flask import Flask, render_template, flash, redirect, url_for
from include.forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '4a7649d351c052cc24f8f64f3a95f580'


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


if __name__ == '__main__':
    app.run(debug = True)