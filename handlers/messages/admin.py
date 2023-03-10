from typing import List

from telegram.ext import MessageHandler, filters

from functions import go_admin


def get_admin_messages_handlers() -> List[MessageHandler]:
    return [
        MessageHandler(filters.Regex("^Режим администратора$"), go_admin),
    ]
