from typing import List

from telegram.ext import MessageHandler, filters

from functions import get_start, get_help


def get_basic_messages_handlers() -> List[MessageHandler]:
    return [
        MessageHandler(filters.Regex("^Начать$"), get_start),
        MessageHandler(filters.Regex("^Правила$"), get_help),
    ]
