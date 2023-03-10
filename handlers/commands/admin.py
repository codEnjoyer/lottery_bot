from typing import List

from telegram.ext import CommandHandler

from functions import go_admin


def get_admin_commands_handlers() -> List[CommandHandler]:
    return [
        CommandHandler("admin", go_admin),
    ]
