from extensions import db

class Variable(db.Model):
    __tablename__ = "variables"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
