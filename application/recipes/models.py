from application import db
from application.ingredients import models

# Change to db.Model() to access 'amount'
#recipe_ingredients = db.Table('recipe_ingredient',
#                             db.Column('recipe_id', db.Integer, db.ForeignKey(
#                                 'recipe.id'), primary_key=True),
#                             db.Column('ingredient_id', db.Integer, db.ForeignKey(
#                                 'ingredient.id'), primary_key=True),
#                             db.Column('amount', db.Integer)
#                             )


class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    amount = db.Column(db.Integer)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(), nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    time = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    ingredients = db.relationship("RecipeIngredient")

    #ingredients = db.relationship('Ingredient', secondary=recipe_ingredients, lazy='subquery',
    #    backref=db.backref('recipes', lazy=True))
 
    def __init__(self, name):
        self.name = name
