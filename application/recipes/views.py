from application import app, db
from flask import render_template, request, redirect, url_for
from application.ingredients.models import Ingredient
from application.recipes.models import Recipe, RecipeIngredient

ingredients_temp = {}
id_temp = {}


@app.route("/recipes/create/", methods=["POST"])
def create_recipe():
    r = Recipe(name=request.form.get("name"))
    r.instructions = request.form.get("instructions")
    db.session().add(r)
    db.session().flush()
    for key, value in id_temp.items():
        ri = RecipeIngredient(recipe_id=r.id, ingredient_id=key, amount=value)
        db.session().add(ri)
    db.session().commit()
    ingredients_temp.clear()
    id_temp.clear()
    return redirect(url_for("recipe_form"))


@app.route("/recipes/new/", methods=["GET"])
def recipe_form():
    return render_template("recipes/new.html", ingredients=Ingredient.query.all(), ingredients_temp=ingredients_temp)


@app.route("/recipes/new", methods=["POST"])
def add_to_recipe():
    i = Ingredient.query.get(request.form.get("id"))
    ingredients_temp[i] = request.form.get("amount")
    id_temp[i.id] = request.form.get("amount")
    return redirect(url_for("recipe_form"))


@app.route("/recipes/clear", methods=["POST"])
def clear_selection():
    key_id = int(request.form.get("key_id"))
    delete = None
    for key, value in ingredients_temp.items():
        if key.id == key_id:
            delete = key
            del id_temp[key.id]
    del ingredients_temp[delete]
    return redirect(url_for("recipe_form"))


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


@app.route("/recipes/<recipe_id>/edit", methods=["GET"])
def edit_recipe(recipe_id):
    r = Recipe.query.get(recipe_id)
    r_i = RecipeIngredient.query.filter_by(recipe_id=r.id).all()
    ingredients = link_amounts(r_i)
    return render_template("recipes/edit.html", recipe=r, ingredients=ingredients)


@app.route("/recipes/<recipe_id>/save", methods=["POST"])
def save_changes(recipe_id):
    r = Recipe.query.get(recipe_id)
    r.name = request.form.get("name")
    r.instructions = request.form.get("instructions")
    db.session.commit()
    return redirect(url_for("view_recipe", recipe_id=recipe_id))


@app.route("/recipes/", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes=Recipe.query.all())


def link_amounts(r_i):
    ingredients = {}
    for item in r_i:
        i = Ingredient.query.get(item.ingredient_id)
        ingredients[i] = item.amount
    return ingredients
