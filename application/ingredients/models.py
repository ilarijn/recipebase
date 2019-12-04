from application import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    unit = db.Column(db.String(20), nullable=True)
    kcal = db.Column(db.Integer)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
   
    def __hash__(self):
        return hash((self.name, self.id))

    def __eq__(self, other):
        return (self.id) == (other.id) and (self.name) == (other.name)