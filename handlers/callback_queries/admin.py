from typing import List

from telegram.ext import CallbackQueryHandler
from functions.admin.admin import remove_lot_inline_button


def get_admin_callback_query_handlers() -> List[CallbackQueryHandler]:
    return [
        CallbackQueryHandler(remove_lot_inline_button, "^Remove")
    ]
