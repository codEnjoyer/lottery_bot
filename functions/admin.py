import peewee
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

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
