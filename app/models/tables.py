from app.extensions.database import db


class TelegramUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_chat_id = db.Column(db.String(10), unique=True)
    suap_token = db.Column(db.String(300))
