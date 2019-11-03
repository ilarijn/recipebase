from application import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=True)

    def __init__(self, name, category, unit):
        self.name = name
        self.category = category
        self.unit = unit

    def __hash__(self):
        return hash((self.name, self.id))

    def __eq__(self, other):
        return (self.id) == (other.id) and (self.name) == (other.name)