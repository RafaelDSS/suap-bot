import click

from flask import current_app
from flask.cli import with_appcontext


@click.command()
@with_appcontext
def set_telegram_webhook():
    is_webhook_set = current_app.bot.set_webhook(url=current_app.config["WEBHOOK_URL"])

    if is_webhook_set:
        print("Webhook configurado com sucesso.")


def init_app(app):
    app.cli.add_command(set_telegram_webhook)
