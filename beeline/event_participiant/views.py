from http import HTTPStatus

import psycopg2
from flask import jsonify
from flask.views import MethodView
from flask_jwt import current_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from beeline.event_participiant.models import Registration
from beeline.plugins import db


class EventParticipantView(MethodView):

    """Контроллер пользователей."""

    @jwt_required()
    def post(self, event_id=None):
        """Регистрация пользователя."""
        registration = Registration(
            user_id=current_identity.id,
            event_id=event_id,
        )
        db.session.add(registration)
        try:
            db.session.commit()
            message = "Успешно зарегистрирован"
            status_code = HTTPStatus.CREATED
        except IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                message = "Уже зарегистрирован"
                status_code = HTTPStatus.BAD_REQUEST
            elif isinstance(e.orig, psycopg2.errors.ForeignKeyViolation):
                message = "Мероприятие не найдено"
                status_code = HTTPStatus.BAD_REQUEST
            else:
                raise e
            db.session.rollback()
        return jsonify(
            dict(message=message)
        ), status_code
