from flask_admin import Admin
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from beeline.auth import authenticate, current_user

db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
jwt = JWT(
    authentication_handler=authenticate,
    identity_handler=current_user,
)
