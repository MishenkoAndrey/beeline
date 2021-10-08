from werkzeug.security import check_password_hash


def authenticate(username, password):
    from beeline.user.models import User
    user = User.query.filter_by(name=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user


def current_user(payload):
    from beeline.user.models import User
    user = User.query.filter_by(id=payload['identity']).first()
    return user
