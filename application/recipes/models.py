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

    name = db.Column(db.String(144), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    ingredients = db.relationship("RecipeIngredient")

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    account_name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name


    @staticmethod
    def find_recipes_by_ingredient_category(category):
        stmt = text("SELECT DISTINCT Recipe.id FROM Recipe " 
        "LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id "
        "LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id "
        "WHERE (Ingredient.category = :category);").params(category=category)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0]})

        return response
  