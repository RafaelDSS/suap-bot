from telegram import Bot
from telegram.ext import Dispatcher

from app.bot.bot import register_handlers


def init_app(app):
    app.bot = Bot(app.config["BOT_TOKEN"])
    app.dispatcher = Dispatcher(app.bot, update_queue=None, workers=1)

    register_handlers(app.dispatcher)
