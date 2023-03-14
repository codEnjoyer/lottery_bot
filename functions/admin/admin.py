from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from functions.admin.database import get_all_lots

import logging

logger = logging.getLogger(__name__)


async def check_if_is_admin(update: Update) -> bool:
    from main import config
    if update.effective_user.id not in config.tg_bot.admins_id:
        logger.info(
            f"""Пользователь {update.effective_user.first_name} безуспешно попытался перейти в режим администратора""")
        await update.message.reply_text("""Вы не являетесь администратором""")
        return False
    return True


async def go_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_if_is_admin(update):
        return

    logger.info(f"""Пользователь {update.effective_user.first_name} перешёл в режим администратора""")
    reply_keyboard = [["Добавить лот"],
                      ["Удалить лот"],
                      ["Объявить розыгрыш"]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    await update.message.reply_text("""Hello, world!""", reply_markup=reply_markup)


async def remove_lot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for lot in get_all_lots():
        text = f"""Название: {lot["name"]}\n
        Описание: {lot["description"]}\n
        Количество номеров: {lot["numbers_count"]}
        Стоимость одного номера: {lot["number_value"]}\n
        Дата розыгрыша: {lot["draw_time"]}\n
        Дата добавления: {lot["published_at"]}"""
        inline_delete_button = InlineKeyboardButton("Удалить", callback_data=f"{lot['id']}")
        inline_kb = InlineKeyboardMarkup([[inline_delete_button]])
        await update.message.reply_text(text, reply_markup=inline_kb)
