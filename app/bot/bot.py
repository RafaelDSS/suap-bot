from telegram.ext import CallbackQueryHandler, CommandHandler, TypeHandler

from .handlers.help import help_command
from .handlers.login import login_command
from .handlers.middleware import middleware
from .handlers.reportcard import callback_report_card, report_card_command
from .handlers.schedule import callback_class_schedule, class_schedule_command
from .handlers.virtualclasses import callback_virtual_class, callback_virtual_class_actions, callback_virtual_classes, virtual_classes_command
from .handlers.helpers import CallbackTypes, generate_pattern


def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("login", login_command))
    dispatcher.add_handler(CommandHandler("virtualclass", virtual_classes_command))
    dispatcher.add_handler(CommandHandler("reportcard", report_card_command))
    dispatcher.add_handler(CommandHandler("class_schedule", class_schedule_command))

    dispatcher.add_handler(CallbackQueryHandler(virtual_classes_command, pattern=generate_pattern(f'{CallbackTypes.PERIODS}{CallbackTypes.VIRTUAL_CLASSES}')))
    dispatcher.add_handler(CallbackQueryHandler(report_card_command, pattern=generate_pattern(f'{CallbackTypes.PERIODS}{CallbackTypes.REPORT_CARD}')))
    dispatcher.add_handler(CallbackQueryHandler(class_schedule_command, pattern=generate_pattern(f'{CallbackTypes.PERIODS}{CallbackTypes.CLASS_SCHEDULE}')))

    dispatcher.add_handler(CallbackQueryHandler(callback_virtual_classes, pattern=generate_pattern(CallbackTypes.VIRTUAL_CLASSES)))
    dispatcher.add_handler(CallbackQueryHandler(callback_virtual_class, pattern=generate_pattern(CallbackTypes.VIRTUAL_CLASS)))
    dispatcher.add_handler(CallbackQueryHandler(callback_report_card, pattern=generate_pattern(CallbackTypes.REPORT_CARD)))
    dispatcher.add_handler(CallbackQueryHandler(callback_class_schedule, pattern=generate_pattern(CallbackTypes.CLASS_SCHEDULE)))
    dispatcher.add_handler(CallbackQueryHandler(callback_virtual_class_actions, pattern=generate_pattern(CallbackTypes.VIRTUAL_CLASSES_STUDENTS)))
    dispatcher.add_handler(CallbackQueryHandler(callback_virtual_class_actions, pattern=generate_pattern(CallbackTypes.VIRTUAL_CLASSES_MATERIALS)))
    dispatcher.add_handler(CallbackQueryHandler(callback_virtual_class_actions, pattern=generate_pattern(CallbackTypes.VIRTUAL_CLASSES_MINISTERED)))

    dispatcher.add_handler(TypeHandler(object, middleware), group=-1)
