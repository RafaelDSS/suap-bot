from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.extensions.database import db
from app.models.tables import TelegramUser


admin = Admin(name="Painel")


def init_app(app):
    admin.init_app(app)


admin.add_views(ModelView(TelegramUser, db.session))
