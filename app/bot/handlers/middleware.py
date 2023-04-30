from app.bot.handlers.help import help_command
from app.bot.handlers.login import login_command
from .base import *


def middleware(update: Update, context: CallbackContext) -> None:
    token = get_suap_token(update.effective_user.id)

    if not token or token_is_expired(token):
        if (not update.callback_query and update.message.text == '/help'):
            help_command(update, context)
        update.message.reply_text("Você não está logado, clique no botão abaixo para logar.")
        login_command(update, context)
        raise DispatcherHandlerStop
    context.suap = SuapApi(token=token)