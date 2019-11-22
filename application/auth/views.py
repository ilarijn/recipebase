from flask import render_template, request, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, UserForm


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form,
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
            return render_template("auth/signup.html", form=UserForm(), errors = form.errors.items()) 
        else:
            u = User(username=form.username.data,
                 name=form.name.data, password=form.password.data)
            try:
                db.session.add(u)
                db.session.commit()
            except IntegrityError as error:
                db.session.rollback()
                return render_template("auth/signup.html", form=form, errors=["Username already exists"])
            return render_template("auth/loginform.html", form=LoginForm(), success="Account created")


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/admin", methods=["GET"])
@login_required
def view_admin():
    user = User.query.get(current_user.id)
    if user.username == "admin":
        return render_template("auth/admin.html", form=UserForm(), users=User.query.all())
    else:
        abort(403)


@app.route("/auth/admin/new", methods=["POST"])
@login_required
def user_create_admin():
    user = User.query.get(current_user.id)
    form = UserForm(request.form)
    if not form.validate():
        return render_template("auth/admin.html", form=form, users=User.query.all())
    if user.username == "admin":
        u = User(username=form.username.data,
                 name=form.name.data, password=form.password.data)
        try:
            db.session.add(u)
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            return render_template("auth/admin.html", form=form, db_error=error, users=User.query.all())

        return redirect(url_for("view_admin"))
    else:
        abort(403)
