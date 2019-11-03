from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rcp.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from application import views

from application.ingredients import views
from application.ingredients import models
from application.recipes import models
from application.recipes import views

db.create_all()
