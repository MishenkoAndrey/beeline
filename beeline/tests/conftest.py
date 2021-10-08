from datetime import datetime as dt

import pytest
from psycopg2 import connect

from beeline import settings
from beeline.app import create_app
from beeline.event.models import Event
from beeline.event_participiant.models import Registration
from beeline.plugins import db as _db
from beeline.user.models import User


@pytest.fixture(scope="session")
def db(app):
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope="session")
def app():
    config = dict()
    config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI+"_test"
    config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    config['SECRET_KEY'] = 'very_secret_key'
    flask_app = create_app(**config)
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


@pytest.fixture(scope="session")
def user(db):
    user = User(name="test", raw_pass="test")
    db.session.add(user)
    db.session.commit()
    yield user
    Registration.query.delete()
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="session")
def event(db):
    event = Event(
        name="test",
        description="test",
        date=dt.now(),
    )
    db.session.add(event)
    db.session.commit()
    yield event
    db.session.delete(event)
    db.session.commit()


@pytest.fixture(scope="session")
def registration(db, user, event):
    Registration.query.delete()
    db.session.commit()
    print(list(Registration.query.all()), "1233")
    reg = Registration(user_id=user.id, event_id=event.id)
    db.session.add(reg)
    db.session.commit()
    print(list(Registration.query.all()), "1233")
    yield reg
    db.session.delete(reg)
    db.session.commit()


@pytest.fixture(scope="session")
def event_list(db):
    event_1 = Event(
        name="test1",
        description="test1",
        date=dt.now(),
    )
    event_2 = Event(
        name="test2",
        description="test2",
        date=dt.now(),
    )
    reg_user = User(name="test_user", raw_pass="test")
    db.session.add(event_1)
    db.session.add(event_2)
    db.session.add(reg_user)
    db.session.commit()
    reg = Registration(user_id=reg_user.id, event_id=event_1.id)
    db.session.add(reg)
    db.session.commit()
    yield [event_1, event_2]
    db.session.delete(reg)
    db.session.commit()
    db.session.delete(event_1)
    db.session.delete(event_2)
    db.session.delete(reg_user)
    db.session.commit()


@pytest.fixture(scope="session")
def single_event(db):
    event = Event(
        name="single",
        description="single event",
        date=dt.now(),
    )
    user = User(
        name="test",
        raw_pass="test",
    )
    db.session.add(event)
    db.session.add(user)
    db.session.commit()
    registration = Registration(user_id=user.id, event_id=event.id)
    db.session.add(registration)
    yield user, event
    db.session.delete(registration)
    db.session.commit()
    db.session.delete(event)
    db.session.delete(user)
    db.session.commit()
