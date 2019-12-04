from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField, HiddenField, validators
from wtforms.widgets import TextArea, HiddenInput


class RecipeIngredientForm(FlaskForm):

    ingredient_id = IntegerField(widget=HiddenInput(), validators=[validators.Optional()])
    ri_name = StringField(widget=HiddenInput(),
                          validators=[validators.Length(min=2)])
    amount = IntegerField(widget=HiddenInput(), validators = [validators.NumberRange(min=1, max=100000)])
    unit = StringField(widget=HiddenInput(), validators=[validators.Length(
        max=10, message="Unit name is too long.")])

    class Meta:
        csrf = False


class RecipeForm(FlaskForm):

    name = StringField("Recipe name", [validators.Length(
        min=2, max=144, message="Name is too short or too long.")])
    servings = IntegerField("Servings", [validators.NumberRange(
        min=1, max=100000, message="Invalid amount of servings.")])
    instructions = StringField("Instructions", widget=TextArea())
    ingredients = FieldList(FormField(RecipeIngredientForm))

    def validate_ingredients(form, field):
        ingredients = form.ingredients.data
        if not ingredients:
            raise validators.ValidationError("Add at least one ingredient.")

    class Meta:
        csrf = False
