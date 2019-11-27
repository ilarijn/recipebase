from application import db
from application.ingredients import models
from sqlalchemy.sql import text


class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredient.id'))

    amount = db.Column(db.Integer)
    unit = db.Column(db.String)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    ingredients = db.relationship("RecipeIngredient")

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    account_name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def search_by_term(recipe, ingredient, category, term):
        query = ("SELECT DISTINCT Recipe.name, Recipe.account_name, Recipe.id, Recipe.account_id FROM Recipe "
                 "LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id "
                 "LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id "
                 "WHERE ")

        r_query = "(LOWER(Recipe.name) LIKE LOWER(:term))"
        i_query = "(LOWER(Ingredient.name) LIKE LOWER(:term))"
        c_query = "(LOWER(Ingredient.category) LIKE LOWER(:term))"
        term = "%"+term+"%"

        if recipe:
            query += r_query
        if ingredient and recipe:
            query += " OR " + i_query
            if category:
                query += " OR " + c_query
        elif ingredient:
            query += i_query
            if category:
                query += " OR " + c_query
        if recipe and category:
            query += " OR " + c_query
        elif category:
            query += c_query

        stmt = text(query).params(term=term)
        res = db.engine.execute(stmt)
        response = []
        
        for row in res:
            response.append(
                {"name": row[0], "account_name": row[1], "id": row[2], "account_id": row[3]})

        return response
