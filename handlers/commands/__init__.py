from typing import List

from telegram.ext import CommandHandler

from .basic import get_basic_commands_handlers
from .admin import get_admin_commands_handlers


def get_commands_handlers() -> List[CommandHandler]:
    return [
        *get_basic_commands_handlers(),
        *get_admin_commands_handlers(),
    ]
