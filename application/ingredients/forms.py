from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField, validators


class IngredientForm(FlaskForm):

    name = StringField("Ingredient name", [validators.Length(min=2)])
    category = StringField("Category", [validators.Length(min=2)])
    unit = StringField("Unit of measurement", [validators.Length(max=20)])
    kcal = IntegerField("kcal per unit")

    class Meta:
        csrf = False


class RecipeIngredientForm(FlaskForm):

    name = StringField("Ingredient", [validators.Length(min=2)])
    unit = StringField("Unit", [validators.Length(max=10)])


class MultiIngredientForm(FlaskForm):

    list_name = StringField("List name")
    ingredients = FieldList(FormField(RecipeIngredientForm), min_entries=1)
