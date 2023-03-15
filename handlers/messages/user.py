from typing import List

from telegram.ext import MessageHandler, filters

from functions.user import get_lots, get_cart


def get_user_messages_handlers() -> List[MessageHandler]:
    return [
        MessageHandler(filters.Regex("^Разыгрываемые лоты$"), get_lots),
        MessageHandler(filters.Regex("^Корзина$"), get_cart),
    ]
