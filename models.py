from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    hobbies = db.Column(db.PickleType, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
