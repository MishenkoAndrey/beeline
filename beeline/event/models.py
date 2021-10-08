from beeline.plugins import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=120))
    description = db.Column(db.Text())
    date = db.Column(db.DateTime())

    def __repr__(self):
        return f"{self.id}:{self.name}"