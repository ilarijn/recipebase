#Flask
from flask import Flask
app = Flask(__name__)


#Database
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rcp.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


#Application
from application import views

from application.ingredients import views
from application.ingredients import models

from application.recipes import models
from application.recipes import views

from application.auth import models 
from application.auth import views 


# Login
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#Create DB
db.create_all()
