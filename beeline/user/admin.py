from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from wtforms import fields


class UserModelView(ModelView):

    """Вью пользователей."""

    column_exclude_list = ('password_hash',)

    def on_model_change(self, filled_form, model, is_created):
        if is_created:
            model.password_hash = generate_password_hash(model.password_hash)
