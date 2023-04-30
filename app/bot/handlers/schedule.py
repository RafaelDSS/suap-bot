from .base import *
from .common import *


def class_schedule_command(update: Update, context: CallbackContext):
    context.title_view = "Horários de Aula"
    context.callback_type = CallbackTypes.CLASS_SCHEDULE
    common_handler_periods(update, context)


def callback_class_schedule(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_query_data = CallbackQueryData(query.data)
    year, period = callback_query_data.last_item.split("/")
    virtual_period_class = context.suap.virtual_period_classes(year, period)

    if not virtual_period_class.__root__:
        query.answer("Ocorreu algum erro ao buscar os horários de aula para esse período.", show_alert=True)
        return

    class_schedule = process_hours_class(virtual_period_class.__root__)
    data = render_template(
        "bot/class schedule.jinja", class_schedule=class_schedule, enumerate=enumerate
    )

    keyboard = [
        InlineKeyboardButton(
            "🔙 Retornar",
            callback_data=callback_query_data.back(f'{CallbackTypes.PERIODS}{CallbackTypes.CLASS_SCHEDULE}')
        )
    ]
    query.edit_message_text(
        data,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([keyboard]),
    )
