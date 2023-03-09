from typing import List

from telegram.ext import CommandHandler

from .default import *


def get_commands_handlers() -> List[CommandHandler]:
    return [
        *get_basic_commands_handlers(),
    ]
