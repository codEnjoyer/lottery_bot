from typing import List

from telegram.ext import CommandHandler

from functions.user import get_lots, get_cart


def get_user_commands_handlers() -> List[CommandHandler]:
    return [
        CommandHandler('lots', get_lots),
        CommandHandler('cart', get_cart),
    ]
