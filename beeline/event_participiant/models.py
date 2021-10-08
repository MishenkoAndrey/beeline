from beeline.plugins import db


class Registration(db.Model):

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        nullable=False,
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('event.id'),
        primary_key=True,
        nullable=False,
    )

    def __init__(self, user_id, event_id):
        self.event_id = event_id
        self.user_id = user_id
