import os

from helpers_config import get_ngrok_url_proxy


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    BOT_TOKEN = "1252149132:AAGUURA7pir2e8KiCzfQu8eW5UA-r71HyXY"
    SECRET_KEY = "knjhghfjfdfk8s7f8wer772827827877"
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{os.path.join(basedir, 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_URL =  get_ngrok_url_proxy()
    WEBHOOK_URL = APP_URL + SECRET_KEY
    FLASK_ADMIN_SWATCH = "flatly"

    CELERY_CONFIG = dict(
        broker_url="pyamqp://teste:teste@localhost:5672//",
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='America/Bahia',
        enable_utc=True,
        beat_schedule={

        }
    )


class ProductionConfig(Config):
    SECRET_KEY = "rueuwreorjk939393ejrnsldkldlssdlsdlri79"
    DEBUG = False
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
