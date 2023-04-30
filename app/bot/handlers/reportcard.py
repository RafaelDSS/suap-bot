from .base import *
from .common import *


def report_card_command(update: Update, context: CallbackContext):
    context.title_view = "Boletim"
    context.callback_type = CallbackTypes.REPORT_CARD
    common_handler_periods(update, context)


def callback_report_card(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_query_data = CallbackQueryData(query.data)
    year, period = callback_query_data.last_item.split("/")
    report_cards = context.suap.report_card(year, period)

    if not report_cards.__root__:
        query.answer("Não há boletim disponível para esse período.", show_alert=True)
        return

    data = render_template("bot/reportcard.jinja", reportcards=report_cards.__root__)

    keyboard = [
        InlineKeyboardButton(
            "🔙 Retornar",
            callback_data=callback_query_data.back(f'{CallbackTypes.PERIODS}{CallbackTypes.REPORT_CARD}'),
        )
    ]
    query.edit_message_text(
        data,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([keyboard]),
    )
