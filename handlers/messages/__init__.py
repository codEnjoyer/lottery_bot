from typing import List

from telegram.ext import MessageHandler

from .basic import get_basic_messages_handlers
from .echo import get_echo_messages_handlers
from .admin import get_admin_messages_handlers

def get_messages_handlers() -> List[MessageHandler]:
    return [
        *get_basic_messages_handlers(),
        *get_admin_messages_handlers(),
        *get_echo_messages_handlers(),  # must be after command_handlers
    ]
