from application import app, db
from flask import render_template, request, redirect, url_for, json, jsonify
from sqlalchemy.exc import IntegrityError
from application.ingredients.models import Ingredient


@app.route("/ingredients/", methods=["GET"])
def ingredients_index():
    return render_template("ingredients/list.html", ingredients=Ingredient.query.all())


@app.route("/ingredients/new/")
def ingredients_form():
    return render_template("ingredients/new.html")


@app.route("/ingredients/", methods=["POST"])
def ingredients_create():
    i = Ingredient(request.form.get("name"), request.form.get(
        "category"), request.form.get("unit"))
    try:
        db.session().add(i)
        db.session().commit()
    except IntegrityError as error:
        print(error)
    return redirect(url_for("ingredients_index"))


@app.route("/ingredients/list/", methods=["GET"])
def ingredients_json():
    ingredients = Ingredient.query.all()
    json_list = []
    for i in ingredients:
        obj = {attr: value for attr, value in i.__dict__.items() if not str(attr).startswith("_")}
        json_list.append(obj)
    return json.dumps(json_list)
