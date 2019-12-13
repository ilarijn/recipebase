from flask import render_template, request, redirect, url_for, json, abort
from flask_login import login_required, current_user

from application import app, db
from application.ingredients.models import Ingredient
from application.recipes.models import Recipe, RecipeIngredient
from application.recipes.forms import RecipeForm, RecipeIngredientForm


@app.route("/recipes/search/", methods=["GET", "POST"])
def recipes_search():
    account_id = ""
    if current_user.is_authenticated:
        account_id = current_user.id

    if request.method == 'POST':
        results = Recipe.search_by_term(
            recipe=request.form.get("recipe"),
            ingredient=request.form.get("ingredient"),
            category=request.form.get("category"),
            term=request.form.get("search"))

        return render_template("recipes/search.html",
                               results=results,
                               account_id=account_id)

    else:
        return render_template("recipes/search.html",
                               recipes=Recipe.query.all(),
                               account_id=account_id)


@app.route("/recipes/", methods=["GET"])
@login_required
def recipes_index():
    return render_template("recipes/list.html",
                           recipes=Recipe.query.
                           filter_by(account_id=current_user.id).all(),
                           account_id=current_user.id)


@app.route("/recipes/new/", methods=["GET"])
@login_required
def recipes_form():
    return render_template("recipes/form.html",
                           form=RecipeForm(),
                           form_action=url_for("recipes_create"),
                           button_text="Create recipe")


@app.route("/recipes/create/test", methods=["POST"])
@login_required
def recipes_create():
    form = RecipeForm(request.form)

    if not form.validate():
        return render_template("recipes/form.html",
                               form=form,
                               form_action=url_for("recipes_create"),
                               button_text="Create recipe")

    recipe = Recipe(form.name.data.strip())
    recipe.servings = form.servings.data
    recipe.instructions = form.instructions.data
    recipe.account_id = current_user.id
    recipe.account_name = current_user.name

    ingredients = form.ingredients.data

    db.session().add(recipe)
    db.session().flush()

    new = create_ingredients(ingredients, recipe.id)

    db.session().commit()

    return redirect(url_for("recipes_view", recipe_id=recipe.id))


@app.route("/recipes/<recipe_id>/edit", methods=["GET"])
@login_required
def recipes_edit(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if recipe.account_id != current_user.id:
        abort(403)

    form = RecipeForm(obj=recipe)

    for ri_form in form.ingredients:
        ingredient = Ingredient.query.get(ri_form.ingredient_id.data)
        ri_form.ri_name.data = ingredient.name

    return render_template("recipes/form.html",
                           form=form,
                           form_action=url_for(
                               "recipes_save", recipe_id=recipe.id),
                           button_text="Save changes")


@app.route("/recipes/<recipe_id>/save/", methods=["POST"])
@login_required
def recipes_save(recipe_id):
    form = RecipeForm(request.form)

    if not form.validate():
        return render_template("recipes/form.html",
                               form=form,
                               form_action=url_for(
                                   "recipes_save", recipe_id=recipe_id),
                               button_text="Save changes")

    recipe = Recipe.query.get(recipe_id)
    recipe.name = form.name.data.strip()
    recipe.servings = form.servings.data
    recipe.instructions = form.instructions.data

    ingredients = form.ingredients

    id_list = {
        ri_form.ingredient_id.data: ri_form.amount.data for ri_form in ingredients}
    ri_list = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()

    for ingredient in ri_list:
        if str(ingredient.ingredient_id) not in id_list:
            db.session.delete(ingredient)
        else:
            ingredient.amount = id_list.pop(str(ingredient.ingredient_id))

    create_ingredients(
        [item for item in form.ingredients.data if item['ingredient_id'] in id_list], recipe.id)

    db.session.commit()
    return redirect(url_for("recipes_view", recipe_id=recipe.id))


@app.route("/recipes/<recipe_id>/", methods=["GET"])
def recipes_view(recipe_id):
    r = Recipe.query.get(recipe_id)
    r_i = RecipeIngredient.query.filter_by(recipe_id=r.id).all()
    ingredients = link_amounts(r_i)

    account_id = ""
    if current_user.is_authenticated:
        account_id = current_user.id

    kcal_total = ingredients.pop(-1)
    kcal_total /= r.servings
    kcal_total = round(kcal_total)
    missing = ingredients.pop(-1)

    return render_template("recipes/view.html",
                           recipe=r,
                           ingredients=ingredients,
                           missing=missing,
                           kcal_total=kcal_total,
                           account_id=account_id)


@app.route("/recipes/<recipe_id>/delete", methods=["GET"])
@login_required
def recipes_delete(recipe_id):
    r = Recipe.query.get(recipe_id)

    if r.account_id != current_user.id:
        abort(403)

    r_i = RecipeIngredient.query.filter_by(recipe_id=r.id).all()
    for item in r_i:
        db.session.delete(item)

    db.session.delete(r)
    db.session.commit()

    return redirect(url_for("recipes_index"))


# Create RecipeIngredients from a list and add new Ingredients
# if ingredient name is not found in the database (not case-sensitive).
def create_ingredients(ingredients, recipe_id):
    new_ingredients = []

    for i in ingredients:
        ingredient_id = None

        if i['ingredient_id'] == None:
            existing_name = Ingredient.query.filter_by(
                name=i['ri_name'].lower().strip()).first()

            if existing_name:
                ingredient_id = existing_name.id
                i['ri_name'] = existing_name.name

            else:
                new = Ingredient(
                    name=i['ri_name'].strip(),
                    unit=i['unit'],
                    account_id=current_user.id)
                db.session().add(new)
                db.session().flush()
                ingredient_id = new.id
                new_ingredients.append(new)

        else:
            ingredient_id = i['ingredient_id']

        ri = RecipeIngredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            amount=i['amount'],
            unit=i['unit'])
        db.session().add(ri)

    return new_ingredients


# Create a printable list of ingredients for Jinja.
# Calculate a kcal total for ingredients using default unit.
def link_amounts(r_i):
    ingredients = []
    missing = []
    kcal_total = 0.0
    for item in r_i:
        i = Ingredient.query.get(item.ingredient_id)
        if item.unit == i.unit and i.kcal != None:
            kcal_total += item.amount * i.kcal
        else:
            missing.append(i.name)
        ingredients.append({'id': i.id, 'name': i.name,
                            'amount': item.amount, 'unit': item.unit})
    ingredients.append(missing)
    ingredients.append(kcal_total)
    return ingredients
