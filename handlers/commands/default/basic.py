from typing import List

from telegram.ext import CommandHandler

from functions import get_start, get_help


def get_basic_commands_handlers() -> List[CommandHandler]:
    return [
        CommandHandler('start', get_start),
        CommandHandler('help', get_help),
    ]
