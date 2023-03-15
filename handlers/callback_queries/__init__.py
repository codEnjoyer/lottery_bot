from typing import List

from telegram.ext import CallbackQueryHandler

from .admin import get_admin_callback_query_handlers


def get_callback_query_handlers() -> List[CallbackQueryHandler]:
    return [
        *get_admin_callback_query_handlers(),
    ]
