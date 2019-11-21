from application import db
from application.ingredients import models


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
