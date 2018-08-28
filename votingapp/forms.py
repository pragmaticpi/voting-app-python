from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, EqualTo

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=8), EqualTo('password')])

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
