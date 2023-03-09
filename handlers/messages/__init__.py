from typing import List

from telegram.ext import MessageHandler, filters

from .echo import unknown_command, echo


def get_messages_handlers() -> List[MessageHandler]:
    return [
        MessageHandler(filters.COMMAND, unknown_command),  # must be after command_handlers
        MessageHandler(filters.TEXT & (~filters.COMMAND), echo),
    ]
