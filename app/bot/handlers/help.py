from .base import *


@send_typing_action
def help_command(update: Update, context: CallbackContext) -> None:
    data = render_template("bot/help.jinja")
    update.message.reply_text(data)
