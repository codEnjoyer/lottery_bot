from typing import List

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, я такой команды не знаю.")


def get_echo_messages_handlers() -> List[MessageHandler]:
    return [
        MessageHandler(filters.COMMAND, unknown_command),  # must be after command_handlers
        MessageHandler(filters.TEXT & (~filters.COMMAND), echo),
    ]