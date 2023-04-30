from .base import *


@send_typing_action
def login_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.from_user.id
    message_id = update.message.message_id
    secret_key = current_app.config["SECRET_KEY"]
    login_keyboard = lambda url: [[InlineKeyboardButton("Login", url)]]

    message = update.message.reply_text(
        "Faça login no bot com sua conta do SUAP.",
        reply_markup=InlineKeyboardMarkup(login_keyboard("https://suap.ifba.edu.br")),
    )
    message_id = message.message_id
    validation_token = generate_validation_token(chat_id, message_id, secret_key)
    login_url = f'{current_app.config["APP_URL"]}auth/{str(validation_token)}'

    context.bot.edit_message_reply_markup(
        chat_id,
        message_id,
        reply_markup=InlineKeyboardMarkup(login_keyboard(login_url))
    )