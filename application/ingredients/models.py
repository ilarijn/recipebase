from application import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=True)

    def __init__(self, name, type, unit):
        self.name = name
        self.type = type
        self.unit = unit
