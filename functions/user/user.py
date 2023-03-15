from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from functions.database import get_all_lots

import logging

logger = logging.getLogger(__name__)


async def get_lots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lots_count = len(get_all_lots())
    if not lots_count:
        await update.message.reply_text("""К сожалению, список лотов пуст""")
        return
    reply_kb = []
    for index, lot in enumerate(get_all_lots()):
        reply_kb.append([f"{lot['name']}"])
    await update.message.reply_text("""Вот список доступных лотов:""", reply_markup=ReplyKeyboardMarkup(reply_kb))


async def get_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
