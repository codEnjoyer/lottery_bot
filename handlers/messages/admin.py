from typing import List

from telegram.ext import MessageHandler, filters

from functions import go_admin, remove_lot


def get_admin_messages_handlers() -> List[MessageHandler]:
    return [
        MessageHandler(filters.Regex("^Режим администратора$"), go_admin),
        MessageHandler(filters.Regex("^Удалить лот$"), remove_lot),
    ]
