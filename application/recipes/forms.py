from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField, HiddenField, validators
from wtforms.widgets import TextArea


class RecipeIngredientForm(FlaskForm):

    id = HiddenField([validators.Regexp("[0-9]", message="Invalid ingredient id.")])
    name = StringField("Ingredient", [validators.Length(min=2)])
    unit = StringField("Unit", [validators.Length(max=10)])


class MultiIngredientForm(FlaskForm):

    list_name = StringField("List name")
    ingredients = FieldList(FormField(RecipeIngredientForm), min_entries=1)


class RecipeForm(FlaskForm):

    name = StringField("Recipe name", [validators.Length(
        min=2, max=144, message="Name is too short or too long.")])
    servings = IntegerField("Servings", [validators.NumberRange(
        min=1, max=100000, message="Invalid amount of servings.")])
    instructions = StringField("Instructions", widget=TextArea())
