from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField, FloatField, validators
from application.ingredients.models import Ingredient


class IngredientForm(FlaskForm):

    name = StringField("Name", [validators.Length(
        min=2, max=40, message="Name too short or too long.")])

    category = StringField("Category",
                           [validators.Length(min=1, max=30, message="Category too short or too long."),
                            validators.Optional()])

    unit = StringField("Default unit",
                       [validators.Length(max=20, message="Unit name too long."),
                        validators.Optional()])

    kcal = FloatField("Kcal per unit", validators=[validators.Length(max=10000000, message="Kcal value too large."),
                                                   validators.Optional()])

    class Meta:
        csrf = False
