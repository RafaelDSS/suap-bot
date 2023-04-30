from app.bot.handlers.periods import callback_periods, periods_command


def common_handler_periods(update, context):
    if update.callback_query:
        return callback_periods(update, context)
    return periods_command(update, context)
