from flask import jsonify
from flask.views import MethodView
from sqlalchemy import case, func, literal_column

from beeline.event.models import Event
from beeline.event.serializers import schema as event_schema
from beeline.event_participiant.models import Registration
from beeline.user.models import User
from beeline.user.serializers import schema as user_schema


class EventView(MethodView):

    """Контроллер пользователей."""

    def get(self, event_id=None):
        if event_id is None:
            res = self._get_event_list()
        else:
            res = self._get_event(event_id)
        return jsonify(res)

    def _get_event(self, event_id):
        event = Event.query.get_or_404(event_id)
        user_ids = Registration.query.filter_by(
            event_id=event.id
        ).with_entities(Registration.user_id)
        users = User.query.filter(User.id.in_(user_ids))
        dumped = event_schema.dump(event)
        dumped['users'] = user_schema.dump(users, many=True)
        return dumped

    def _get_event_list(self):
        query = Event.query.join(
            Registration,
            Registration.event_id == Event.id,
            isouter=True,
        ).group_by(
            Registration.event_id,
            Event.id,
        ).add_columns(
            case(
                (
                    func.count(
                        Registration.user_id
                    ) > literal_column("0"), literal_column("true")),
                else_=literal_column('false')
            ).label("has_participants")
        )
        # обязательно пагинация должна быть, но это тестовое
        res = []
        for event, has_participants in query:
            dumped = event_schema.dump(event)
            dumped['has_participants'] = has_participants
            res.append(dumped)
        return res
