from functools import wraps

import jwt
from flask import current_app
from telegram import ChatAction

from app.models.tables import TelegramUser


class CallbackTypes:
    """ Enums para indentificação dos callback_query."""
    PERIODS = 1
    REPORT_CARD = 2
    VIRTUAL_CLASS = 3
    VIRTUAL_CLASSES = 4
    VIRTUAL_CLASSES_STUDENTS = 5
    VIRTUAL_CLASSES_MINISTERED = 6
    VIRTUAL_CLASSES_MATERIALS = 7
    CLASS_SCHEDULE = 8


def generate_pattern(type):
    return r"^" + str(type)


class CallbackQueryData:
    """ Helper class to callback_query.data
    Ex: '1 2/2022}'
    """
    def __init__(self, callback_query) -> None:
        self.type, self.data_list = self.__process_callback_query(callback_query)

    @property
    def last_item(self):
        return self.data_list[-1]

    @classmethod
    def from_callback_empty(cls):
        return cls('0')

    def __process_callback_query(self, callback_query):
        data = callback_query.split(' ')
        return data[0], data[1:]

    def advance(self, type, item):
        new_data_list = self.data_list[:]
        new_data_list.append(item)
        return self.repr_str_callback_query(type, new_data_list)

    def back(self, type):
        self.data_list.pop(-1)
        return self.repr_str_callback_query(type, self.data_list)

    def repr_str_callback_query(self, type, data_list):
        return f'{type} {" ".join(str(item) for item in data_list)}'


def get_suap_token(user_id):
    """Recupera o token a partir do user_id do Telegram.

    :param user_id:
    :return suap_token:
    """
    with current_app.app_context():
        telegram_user = TelegramUser.query.filter_by(telegram_chat_id=user_id).first()

    if telegram_user:
        return telegram_user.suap_token
    return None


def generate_validation_token(chat_id, message_id, secret_key):
    encoded_jwt = jwt.encode(
        {"chat_id": chat_id, "message_id": message_id}, secret_key, algorithm="HS256"
    )
    return encoded_jwt


def get_payload_from_token(encoded_jwt, secret_key):
    decoded_jwt = jwt.decode(encoded_jwt, secret_key, algorithms=["HS256"])
    return decoded_jwt


def token_is_expired(token):
    """Verifica a expiração do token.

    :param token:
    :return boolean:
    """
    try:
        jwt.decode(token, leeway=-100, algorithms=["HS256"], options={'verify_signature': False, "verify_exp": True})
    except jwt.ExpiredSignatureError:
        return True
    return False


def send_typing_action(func):
    """Envia a ação de digitando enquando processa o comando da função."""

    @wraps(func)
    def command_func(*args, **kwargs):
        update, context = args
        context.bot.send_chat_action(
            chat_id=update.message.from_user.id or update.callback_query.from_user.id, action=ChatAction.TYPING
        )
        func(*args, **kwargs)

    return command_func


def process_hours_class(virtual_classes):
    """ Transforma os dados de horário do SUAP em uma Matriz.

    :param virtual_classes:
    :return hour_formatted:
            A primeira coluna contem os horários, as outras são as aulas
            de segunda a sexta com seus respectivos horários.
            Ex:
            [
                ["horário1", aula1, aula2, aula3, aula4, aula5],
                ["horário2", aula1, aula2, aula3, aula4, aula5],
            ]
    """
    hours = [
        "13:00 - 13:50",
        "13:50 - 14:40",
        "14:40 - 15:30",
        "15:30 - 16:20",
        "16:40 - 17:30",
        "17:30 - 18:20",
    ]

    formatted_hour = list(map(lambda x: [x, *(5 * [None])], hours))

    for item in virtual_classes:
        hours_discipline = item.horarios_de_aula.split(" / ")

        for hour in hours_discipline:
            day = int(hour[0]) - 1

            for i in range(2, len(hour)):
                slot = int(hour[i]) - 1
                formatted_hour[slot][day] = item.descricao
    return formatted_hour
