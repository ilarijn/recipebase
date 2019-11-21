from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class UserForm(FlaskForm):
    name = StringField("Name")
    username = StringField("Username", [validators.Length(min=2)])
    password = PasswordField("Password", [validators.Length(min=4)])

    class Meta:
        csrf = False
