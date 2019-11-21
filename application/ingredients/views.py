from application import app, db
from flask import render_template, request, redirect, url_for, json, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from application.ingredients.models import Ingredient
from application.ingredients.forms import IngredientForm


@app.route("/ingredients/", methods=["GET"])
@login_required
def ingredients_index():
    return render_template("ingredients/list.html", ingredients=Ingredient.query.all())


@app.route("/ingredients/new/", methods=["GET"])
@login_required
def ingredients_form():
    return render_template("ingredients/new.html", form=IngredientForm())


@app.route("/ingredients/", methods=["POST"])
@login_required
def ingredients_create():
    form = IngredientForm(request.form)
    if not form.validate():
        return render_template("ingredients/new.html", form=form)
    i = Ingredient(name=form.name.data, category=form.category.data,
                   unit=form.unit.data)
    kcal = form.kcal.data
    if kcal == "":
        kcal == None
    i.kcal = kcal
    try:
        db.session().add(i)
        db.session().commit()
    except IntegrityError as error:
        print(error)
    return redirect(url_for("ingredients_index"))


@app.route("/ingredients/list/", methods=["GET"])
@login_required
def ingredients_json():
    ingredients = Ingredient.query.all()
    json_list = []
    for i in ingredients:
        obj = {attr: value for attr, value in i.__dict__.items()
               if not str(attr).startswith("_")}
        json_list.append(obj)
    return json.dumps(json_list)


@app.route("/ingredients/new/", methods=["POST"])
@login_required
def update_json():
    ingredients = request.get_json()
    for i in ingredients:
        update = Ingredient.query.get(int(i['id']))
        update.category = i['category']
        update.unit = i['unit']
        if update.kcal != "":
            update.kcal = i['kcal']
        else:
            update.kcal = None
    db.session.commit()
    return redirect(url_for("recipes_index"))
