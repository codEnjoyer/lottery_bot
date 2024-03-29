from typing import List

from telegram.ext import CommandHandler

from .basic import get_basic_commands_handlers
from .admin import get_admin_commands_handlers
from .user import get_user_commands_handlers
from functions.admin import get_add_lot_conversation_handler


def get_commands_handlers() -> List[CommandHandler]:
    return [
        get_add_lot_conversation_handler(),
        *get_user_commands_handlers(),
        *get_basic_commands_handlers(),
        *get_admin_commands_handlers(),
    ]
