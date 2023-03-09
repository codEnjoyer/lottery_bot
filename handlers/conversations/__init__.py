from typing import List

from telegram.ext import ConversationHandler

from .bio import get_bio_handler
from .facts import get_facts_handler


def get_conversations_handlers() -> List[ConversationHandler]:
    return [
        get_bio_handler(),
        get_facts_handler()
    ]
