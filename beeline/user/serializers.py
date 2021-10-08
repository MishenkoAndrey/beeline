from marshmallow import Schema, fields


class Event(Schema):

    """Схема списка мероприятий."""

    id = fields.Integer()
    name = fields.String()


schema = Event()
