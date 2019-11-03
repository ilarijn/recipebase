from application import db
from application.ingredients import models


recipeingredients = db.Table('recipeingredient',
                             db.Column('recipe_id', db.Integer, db.ForeignKey(
                                 'recipe.id'), primary_key=True),
                             db.Column('ingredient_id', db.Integer, db.ForeignKey(
                                 'ingredient.id'), primary_key=True),
                             db.Column('amount', db.Integer)
                             )

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    time = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    ingredients = db.relationship('Ingredient', secondary=recipeingredients, lazy='subquery',
        backref=db.backref('recipes', lazy=True))
 
    def __init__(self, name):
        self.name = name
