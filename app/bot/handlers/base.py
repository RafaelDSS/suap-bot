from dataclasses import dataclass
from pprint import pprint

from flask import current_app, render_template
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update)
from telegram.ext import (CallbackContext, DispatcherHandlerStop)

from ..suap_wrapper.main import SuapApi
from .helpers import (generate_validation_token, get_suap_token,
                    process_hours_class, send_typing_action, token_is_expired, CallbackQueryData, CallbackTypes)