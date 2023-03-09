from typing import List

from telegram.ext import CommandHandler

from .basic import start_command, help_command


def get_basic_commands_handlers() -> List[CommandHandler]:
    return [
        CommandHandler('start', start_command),
        CommandHandler('help', help_command),
    ]
