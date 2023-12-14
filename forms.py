from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    manager_code = StringField('Manager Code (optional)')  # Add this line
# Above is the registration form with the username, password, confirm password, and manager code field with the respective validators

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
# Above is the login form using flask, with the username and password fields with the respective validators