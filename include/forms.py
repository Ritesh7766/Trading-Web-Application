from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=5, max=40)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Register')


class LoginForm(FlaskForm):
    email = StringField()
    password = PasswordField()
    submit = SubmitField(label = 'Log In')