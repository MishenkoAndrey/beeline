from werkzeug.security import generate_password_hash

from beeline.plugins import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=120), unique=True)
    password_hash = db.Column(db.String())

    def __init__(self, name, raw_pass):
        self.name = name
        self.password_hash = generate_password_hash(raw_pass)

    def __str__(self):
        return self.name
