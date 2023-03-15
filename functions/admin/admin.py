from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from functions.database import get_all_lots, delete_lot

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
    if not len(get_all_lots()):
        await update.message.reply_text("""Список лотов пуст!""")
        return
    for lot in get_all_lots():
        text = f"""Название: {lot["name"]}\n
        Описание: {lot["description"]}\n
        Количество номеров: {lot["numbers_count"]}
        Стоимость одного номера: {lot["number_value"]}\n
        Дата розыгрыша: {lot["draw_time"]}\n
        Дата добавления: {lot["published_at"]}"""
        inline_delete_button = InlineKeyboardButton("Удалить", callback_data=f"Remove_lot {lot['id']}")
        inline_kb = InlineKeyboardMarkup([[inline_delete_button]])
        await update.message.reply_photo(lot["image_id"], text, reply_markup=inline_kb)


async def remove_lot_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        lot_id = int(query.data.split()[1])
        logger.info(f"Лот с {lot_id=} подготавливается к удалению")
    except ValueError:
        await update.message.reply_text("""Не удалось удалить лот""")
        return
    delete_lot(lot_id)
    logger.info(f"Лот с {lot_id=} был удалён")
    await query.answer("""Лот был успешно удалён""")
