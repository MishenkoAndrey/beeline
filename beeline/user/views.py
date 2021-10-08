from flask.views import MethodView


class UserController(MethodView):

    """Контроллер пользователей."""

    def post(self):
        """Регистрация пользователя."""
        return {}

    def get(self, user_id):
        return {"user": user_id}

    def put(self, user_id):
        return {"user": user_id}
