from application import app, db
from flask import render_template, request, redirect, url_for, json, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from application.ingredients.models import Ingredient
from application.ingredients.forms import IngredientForm
from application.recipes.models import RecipeIngredient


@app.route("/ingredients/", methods=["GET"])
@login_required
def ingredients_index():
    return render_template("ingredients/list.html",
                           ingredients=Ingredient.query.order_by(
                               func.lower(Ingredient.name)).all(),
                           form=IngredientForm(),
                           form_action=url_for("ingredients_create"),
                           button_text="Add Ingredient")


@app.route("/ingredients/<ingredient_id>/edit", methods=["GET"])
@login_required
def ingredients_edit(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    form = IngredientForm(obj=ingredient)

    return render_template("ingredients/list.html",
                           ingredients=Ingredient.query.order_by(
                               func.lower(Ingredient.name)).all(),
                           form=form,
                           form_action=url_for(
                               "ingredients_save", ingredient_id=ingredient_id),
                           button_text="Save Changes")


@app.route("/ingredients/<ingredient_id>/edit/", methods=["POST"])
@login_required
def ingredients_save(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    form = IngredientForm(request.form, obj=ingredient)
    if not form.validate():
        return render_template("ingredients/list.html",
                               ingredients=Ingredient.query.order_by(
                                   func.lower(Ingredient.name)).all(),
                               form=form,
                               form_action=url_for(
                                   "ingredients_save", ingredient_id=ingredient_id),
                               button_text="Save Changes")
    form.populate_obj(ingredient)
    try:
        db.session().commit()
        return redirect(url_for("ingredients_index"))
    except IntegrityError as error:
        db.session.rollback()
        return render_template("ingredients/list.html",
                               ingredients=Ingredient.query.order_by(
                                   func.lower(Ingredient.name)).all(),
                               form=form,
                               form_action=url_for(
                                   "ingredients_save", ingredient_id=ingredient_id),
                               db_error="Ingredient name already exists.",
                               button_text="Save Changes")


@app.route("/ingredients/", methods=["POST"])
@login_required
def ingredients_create():
    form = IngredientForm(request.form)
    if not form.validate():
        return render_template("ingredients/list.html",
                               ingredients=Ingredient.query.all(),
                               form=form,
                               form_action=url_for("ingredients_create"),
                               button_text="Add Ingredient")

    i = Ingredient(name=form.name.data, category=form.category.data,
                   unit=form.unit.data)
    kcal = form.kcal.data
    i.kcal = kcal
    try:
        db.session().add(i)
        db.session().commit()
        return redirect(url_for("ingredients_index"))
    except IntegrityError as error:
        db.session.rollback()
        return render_template("ingredients/list.html",
                               ingredients=Ingredient.query.order_by(
                                   func.lower(Ingredient.name)).all(),
                               form=form,
                               form_action=url_for(
                                   "ingredients_create"),
                               db_error="Ingredient name already exists.",
                               button_text="Add Ingredient")


@app.route("/ingredients/<ingredient_id>/delete", methods=["GET"])
@login_required
def ingredients_delete(ingredient_id):
    i = Ingredient.query.get(ingredient_id)
    r_i = RecipeIngredient.query.filter_by(ingredient_id=i.id).all()
    if r_i:
        return render_template("ingredients/list.html",
                               ingredients=Ingredient.query.order_by(
                                   func.lower(Ingredient.name)).all(),
                               form=IngredientForm(),
                               form_action=url_for(
                                   "ingredients_create"),
                               db_error="Ingredient is used in a recipe.",
                               button_text="Add Ingredient")
    else:
        db.session.delete(i)
        db.session.commit()
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
        if str(i['kcal']).isnumeric():
            update.kcal = int(i['kcal'])
        else:
            update.kcal = None
    db.session.commit()
    return redirect(url_for("recipes_index"))
