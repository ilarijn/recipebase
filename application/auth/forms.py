from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from application import db
from application.auth.models import User


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class UserForm(FlaskForm):
    name = StringField("Name", [validators.Length(
        min=2, max=30, message="Name must be between 2 and 30 characters."),
        validators.Regexp('^[\w ]+$', message="Name can only contain alphanumeric characters.")])
    username = StringField("Username", [validators.Length(
        min=4, max=20, message="Username must be between 4 and 20 characters."),
        validators.Regexp('^\w+$', message="Username can only contain alphanumeric characters.")])
    password = PasswordField("Password", [validators.Length(
        min=4, max=30, message="Password must be between 4 and 30 characters.")])

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise validators.ValidationError("Username already exists.")

    class Meta:
        csrf = False
