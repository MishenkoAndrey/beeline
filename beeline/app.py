from logging import NullHandler, StreamHandler
from sys import stdout

from flask import Flask
from flask_admin.contrib.sqla import ModelView

from beeline import settings
from beeline.event.models import Event
from beeline.event.views import EventView
from beeline.event_participiant.views import EventParticipantView
from beeline.plugins import admin, db, jwt, migrate
from beeline.user.admin import UserModelView
from beeline.user.models import User


def init_plugins(app):
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    register_admin()
    jwt.init_app(app)


def register_admin():
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(ModelView(Event, db.session))


def register_urls(app):
    event_view = EventView.as_view('event_resource')
    event_participant_view = EventParticipantView.as_view(
        'registration_resource'
    )
    app.add_url_rule(
        '/event/',
        view_func=event_view,
        methods=['POST',]
    )
    app.add_url_rule(
        '/event/<int:event_id>',
        view_func=event_view,
        methods=['GET', ]
    )
    app.add_url_rule(
        '/event/',
        view_func=event_view,
        methods=['GET', ]
    )
    app.add_url_rule(
        '/registration/<int:event_id>/',
        view_func=event_participant_view,
        methods=['POST', ]
    )


def register_error_handlers(app):
    pass


def set_settings(app, **config):
    for key, val in config.items():
        app.config[key] = val


def create_app(**config):
    app = Flask("beeline")
    set_settings(app, **config)
    init_plugins(app)
    register_urls(app)
    register_error_handlers(app)
    if settings.DEBUG:
        handler = StreamHandler(stdout)
    else:
        handler = NullHandler()
    app.logger.addHandler(handler)
    return app
