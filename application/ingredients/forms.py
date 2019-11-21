from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators


class IngredientForm(FlaskForm):
    name = StringField("Ingredient name", [validators.Length(min=2)])
    category = StringField("Category", [validators.Length(min=2)])
    unit = StringField("Unit of measurement", [validators.Length(max=10)])
    kcal = IntegerField("kcal per unit")

    class Meta:
        csrf = False
