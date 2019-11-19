from flask import render_template, request, redirect, url_for, json, abort
from flask_login import login_required, current_user

from application import app, db
from application.ingredients.models import Ingredient
from application.recipes.models import Recipe, RecipeIngredient


@app.route("/recipes/", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes=Recipe.query.all())


@app.route("/recipes/new/", methods=["GET"])
def recipe_form():
    return render_template("recipes/new.html")


@app.route("/recipes/create/", methods=["POST"])
def create_recipe():
    if current_user.is_authenticated:
        data = request.get_json()
        name = data['name']
        instructions = data['instructions']
        ingredients = data['ingredients']

        r = Recipe(name)
        r.instructions = instructions
        r.account_id = current_user.id

        db.session().add(r)
        db.session().flush()

        create_ingredients(ingredients, r.id)

        db.session().commit()
        return "OK"

    else:
        abort(400)


@app.route("/recipes/<recipe_id>/edit", methods=["GET"])
def edit_recipe(recipe_id):
    r = Recipe.query.get(recipe_id)
    r_i = RecipeIngredient.query.filter_by(recipe_id=r.id).all()
    ingredients = link_amounts(r_i)
    return render_template("recipes/edit.html", recipe=r, ingredients=ingredients)


@app.route("/recipes/<recipe_id>/save/", methods=["POST"])
def save_changes(recipe_id):
    data = request.get_json()
    r = Recipe.query.get(recipe_id)
    r.name = data['name']
    r.instructions = data['instructions']
    ingredients = data['ingredients']

    id_list = {item['id']: item['amount'] for item in ingredients}
    ri_list = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()

    for ingredient in ri_list:
        if str(ingredient.ingredient_id) not in id_list:
            db.session.delete(ingredient)
        else:
            ingredient.amount = id_list.pop(str(ingredient.ingredient_id))

    create_ingredients(
        [item for item in ingredients if item['id'] in id_list], r.id)

    db.session.commit()
    return "OK"


@app.route("/recipes/<recipe_id>/", methods=["GET"])
def view_recipe(recipe_id):
    r = Recipe.query.get(recipe_id)
    r_i = RecipeIngredient.query.filter_by(recipe_id=r.id).all()
    ingredients = link_amounts(r_i)
    return render_template("recipes/view.html", recipe=r, ingredients=ingredients)


@app.route("/recipes/<recipe_id>/delete", methods=["POST"])
def delete_recipe(recipe_id):
    r = Recipe.query.get(recipe_id)
    r_i = RecipeIngredient.query.filter_by(recipe_id=r.id).all()
    for item in r_i:
        db.session.delete(item)
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for("recipes_index"))


def create_ingredients(ingredients, recipe_id):
    for i in ingredients:
        ingredient_id = None
        if i['id'] == "":
            new = Ingredient(
                name=i['name'], unit=i['unit'], category=i['category'])
            if i['kcal'] != "":
                new.kcal = int(i['kcal'])
            db.session().add(new)
            db.session().flush()
            ingredient_id = new.id
        else:
            ingredient_id = i['id']
        ri = RecipeIngredient(
            recipe_id=recipe_id, ingredient_id=ingredient_id, amount=i['amount'])
        db.session().add(ri)
    return


def link_amounts(r_i):
    ingredients = {}
    for item in r_i:
        i = Ingredient.query.get(item.ingredient_id)
        ingredients[i] = item.amount
    return ingredients
