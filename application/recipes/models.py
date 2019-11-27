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

        term = "%"+term+"%"

        r_query = ("SELECT Recipe.id, Recipe.name, Recipe.account_id, Recipe.account_name FROM Recipe "
                   "WHERE (LOWER(Recipe.name) LIKE LOWER(:term));")
        i_query = ("SELECT Recipe.id, Recipe.name, Recipe.account_id, Recipe.account_name, Ingredient.name as ingredient FROM Recipe "
                   "LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id "
                   "LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id LEFT JOIN "
                   "(SELECT Recipe.name, Recipe.id as id, COUNT(Recipe.id) as count FROM Recipe "
                   "LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id "
                   "LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id "
                   "WHERE (LOWER(Ingredient.name) LIKE LOWER(:term)) GROUP BY Recipe.id) as matches ON matches.id = Recipe.id "
                   "WHERE (LOWER(Ingredient.name) LIKE LOWER(:term)) ORDER BY matches.count DESC;")
        c_query = ("SELECT Recipe.id, Recipe.name, Recipe.account_id, Recipe.account_name, Ingredient.category as category FROM Recipe "
                   "LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id "
                   "LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id LEFT JOIN "
                   "(SELECT Recipe.name, Recipe.id as id, COUNT(Recipe.id) as count FROM Recipe "
                   "LEFT JOIN Recipe_Ingredient ON Recipe_Ingredient.recipe_id = Recipe.id "
                   "LEFT JOIN Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id "
                   "WHERE (LOWER(Ingredient.category) LIKE LOWER(:term)) GROUP BY Recipe.id ) as matches ON matches.id = Recipe.id "
                   "WHERE (LOWER(Ingredient.category) LIKE LOWER(:term)) ORDER BY matches.count DESC;")

        response = {}

        if ingredient:
            stmt = text(i_query).params(term=term)
            res = db.engine.execute(stmt)
            prev_id = None
            for row in res:
                if row[0] == prev_id:
                    response[prev_id]['ingredient_matches'].append(row[4])
                else:
                    response[row[0]] = {'id': row[0], 'name': row[1], 'account_id': row[2],
                                        'account_name': row[3], 'ingredient_matches': [row[4]]}
                    prev_id = row[0]

        if category:
            stmt = text(c_query).params(term=term)
            res = db.engine.execute(stmt)
            prev_id = None
            for row in res:
                if row[0] == prev_id:
                    response[prev_id]['category_matches'].append(row[4])
                elif not row[0] in response:
                    response[row[0]] = {'id': row[0], 'name': row[1], 'account_id': row[2],
                                        'account_name': row[3], 'category_matches': [row[4]]}
                    prev_id = row[0]
                else:
                    response[row[0]]['category_matches'] = [row[4]]
                    prev_id = row[0]

        if recipe:
            stmt = text(r_query).params(term=term)
            res = db.engine.execute(stmt)
            for row in res:
                if not row[0] in response:
                    response[row[0]] = {
                        'id': row[0], 'name': row[1], 'account_id': row[2], 'account_name': row[3]}

        return response
