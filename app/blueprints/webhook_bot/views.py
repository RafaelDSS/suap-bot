import telegram

from flask import Blueprint, request, current_app, Response

app_webhook_bot = Blueprint("bot", __name__)


@app_webhook_bot.route("/<secret_key>", methods=["POST"])
def content_from_webhook(secret_key=None):
    if secret_key == current_app.config["SECRET_KEY"]:
        update = telegram.update.Update.de_json(
            request.get_json(force=True), current_app.bot
        )
        current_app.dispatcher.process_update(update)

    return Response(status=200)


def init_app(app):
    app.register_blueprint(app_webhook_bot)
