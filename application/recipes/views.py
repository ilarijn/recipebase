from application import app, db
from flask import render_template, request, redirect, url_for
from application.ingredients.models import Ingredient
from application.recipes.models import Recipe

r = Recipe("")
ingredients_temp = {}

@app.route("/recipes/new", methods=["GET"])
def recipe_form():
    return render_template("recipes/new.html", ingredients=Ingredient.query.all(), ingredients_temp=ingredients_temp)

@app.route("/recipes/new", methods=["POST"])
def add_to_recipe():
    i = Ingredient.query.get(request.form.get("id"))
    ingredients_temp[i] = request.form.get("amount")
    return render_template("recipes/new.html", ingredients=Ingredient.query.all(), ingredients_temp=ingredients_temp)

@app.route("/recipes/clear", methods=["POST"])
def clear_selection():
    ingredients_temp.clear()
    return redirect(url_for("recipe_form"))
