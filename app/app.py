from flask import Flask

from app.extensions import database, migrate, bot, admin, cli, celery
from app.blueprints import webhook_bot, auth
from app.bot import tasks


# Factory App
def create_app(config="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config)

    # Extensions
    database.init_app(app)
    migrate.init_app(app)
    bot.init_app(app)
    admin.init_app(app)
    cli.init_app(app)
    celery.init_app(app)

    # Blueprints
    webhook_bot.views.init_app(app)
    auth.views.init_app(app)

    return app
