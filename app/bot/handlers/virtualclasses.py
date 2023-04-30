from .base import *
from .common import *


def virtual_classes_command(update: Update, context: CallbackContext):
    context.title_view = "Salas Virtuais"
    context.callback_type = CallbackTypes.VIRTUAL_CLASSES
    common_handler_periods(update, context)

def callback_virtual_classes(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_query_data = CallbackQueryData(query.data)
    year, period = callback_query_data.last_item.split("/")
    virtual_period_classes = context.suap.virtual_period_classes(year, period)

    if not virtual_period_classes.__root__:
        query.answer("Não há Salas Virtuais disponíveis para esse período.", show_alert=True)
        return

    keyboard = []
    for virtual_class in virtual_period_classes.__root__:
        keyboard.append(
            {
                InlineKeyboardButton(
                    virtual_class.descricao,
                    callback_data=callback_query_data.advance(CallbackTypes.VIRTUAL_CLASS, virtual_class.id),
                )
            }
        )
    keyboard.append(
        {
            InlineKeyboardButton(
                "🔙 Retornar",
                callback_data=callback_query_data.back(f'{CallbackTypes.PERIODS}{CallbackTypes.VIRTUAL_CLASSES}'),
            )
        }
    )
    query.edit_message_text(
        "Selecione uma disciplina:",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def callback_virtual_class(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    callback_query_data = CallbackQueryData(query.data)
    virtual_class_id = callback_query_data.last_item

    keyboard = []

    actions_to_virtual_class = (
        ("Alunos da disciplina", CallbackTypes.VIRTUAL_CLASSES_STUDENTS),
        ("Materiais", CallbackTypes.VIRTUAL_CLASSES_MATERIALS),
        ("Aulas ministradas", CallbackTypes.VIRTUAL_CLASSES_MINISTERED),
    )

    for action in actions_to_virtual_class:
        keyboard.append(
            [
                InlineKeyboardButton(
                    action[0],
                    callback_data=callback_query_data.advance(action[1], virtual_class_id),
                )
            ],
        )

    keyboard.append(
        [InlineKeyboardButton("🔙 Retornar", callback_data=callback_query_data.back(CallbackTypes.VIRTUAL_CLASSES))],
    )
    query.edit_message_text(
        "Selecione uma opção:",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def callback_virtual_class_actions(update: Update, context: CallbackContext) -> None:
    templates_name = {
        CallbackTypes.VIRTUAL_CLASSES_STUDENTS: "virtual_class_students",
        CallbackTypes.VIRTUAL_CLASSES_MATERIALS: "virtual_class_materials",
        CallbackTypes.VIRTUAL_CLASSES_MINISTERED: "virtual_class_ministred",
    }
    query = update.callback_query
    callback_query_data = CallbackQueryData(query.data)
    class_id= callback_query_data.last_item
    template_type = callback_query_data.type

    print(template_type)

    virtual_class = context.suap.virtual_class(class_id)
    data = render_template(
        f"bot/{templates_name[int(template_type)]}.jinja",
        virtual_class=virtual_class,
        enumerate=enumerate,
    )

    keyboard = query.message.reply_markup.inline_keyboard

    query.answer()
    query.edit_message_text(
        data,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
