from .base import *


def generate_keyboard_periods(context, periods):
    callback_query_data = CallbackQueryData.from_callback_empty()
    keyboard = []

    for period in periods.__root__:
        period_str = f"{period.ano_letivo}/{period.periodo_letivo}"
        keyboard.append(
            {
                InlineKeyboardButton(
                    f'➡️ {period_str}',
                    callback_data=callback_query_data.advance(context.callback_type, period_str),
                )
            }
        )

    return keyboard


@send_typing_action
def periods_command(update: Update, context: CallbackContext) -> None:
    periods = context.suap.list_periods()

    keyboard = generate_keyboard_periods(context, periods)
    update.message.reply_text(
        f"{context.title_view} \- Selecione um dos períodos:",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def callback_periods(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    periods = context.suap.list_periods()

    keyboard = generate_keyboard_periods(context, periods)
    query.edit_message_text(
        f"{context.title_view} \- Selecione um dos períodos:",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
