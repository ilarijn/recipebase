from flask import render_template, request, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, UserForm


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/login.html", form=LoginForm())

    form = LoginForm(request.form)
    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()

    if not user:
        return render_template("auth/login.html", form=form,
                               error="Incorrect username or password")

    login_user(user)
    print("User " + user.name + " logged in")
    return redirect(url_for("index"))


@app.route("/auth/new", methods=["GET", "POST"])
def auth_signup():
    if request.method == "GET":
        return render_template("auth/signup.html", form=UserForm())

    else:
        form = UserForm(request.form)
        if not form.validate():
            return render_template("auth/signup.html", form=form)

        else:
            user = User(username=form.username.data,
                        name=form.name.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return render_template("auth/login.html", form=LoginForm(), success="Account created.")


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))