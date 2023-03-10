from typing import List

from telegram.ext import CommandHandler

from functions import go_admin, remove_lot


def get_admin_commands_handlers() -> List[CommandHandler]:
    return [
        CommandHandler("admin", go_admin),
        CommandHandler("remove_lot", remove_lot),
    ]
