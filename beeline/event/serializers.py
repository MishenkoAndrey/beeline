from marshmallow import Schema, fields


class Event(Schema):

    """Схема списка мероприятий."""

    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    date = fields.DateTime(
        format='%Y-%m-%dT%H:%M:%S%z',
    )


schema = Event()
