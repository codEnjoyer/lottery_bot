import datetime as dt
# from pytz import timezone
from zoneinfo import ZoneInfo
import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from functions.admin import database

GET_NAME, GET_DESCRIPTION, GET_NUMBERS_COUNT, GET_PHOTO, GET_NUMBER_VALUE, GET_DRAW_TIME, DO_FINAL_CHECK = range(7)
logger = logging.getLogger(__name__)
cancel_markup = ReplyKeyboardMarkup([["Отмена"]], one_time_keyboard=True, resize_keyboard=True)


async def start_adding_lot_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""

    await update.message.reply_text(
        """Введите название лота""",
        reply_markup=cancel_markup
    )

    return GET_NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    input_name = update.message.text
    context.user_data["name"] = input_name
    await update.message.reply_text(
        """Введите описание лота""",
        reply_markup=cancel_markup
    )

    return GET_DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    input_description = update.message.text
    context.user_data["description"] = input_description
    await update.message.reply_text(
        """Загрузите изображение для лота""",
        reply_markup=cancel_markup
    )

    return GET_PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    image_id = update.message.photo[0].file_id
    context.user_data["image_id"] = image_id
    await update.message.reply_text(
        """Введите количество номеров для лота""",
        reply_markup=cancel_markup
    )

    return GET_NUMBERS_COUNT


async def numbers_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    if not update.message.text.strip().isdigit():
        await update.message.reply_text("Некорректно введённое число. Повторите ввод")
        return GET_NUMBERS_COUNT

    input_numbers_count = update.message.text
    context.user_data["numbers_count"] = int(input_numbers_count)
    await update.message.reply_text(
        """Введите цену за один номер""",
        reply_markup=cancel_markup
    )

    return GET_NUMBER_VALUE


async def number_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    if not update.message.text.strip().isdigit():
        await update.message.reply_text("Некорректно введённое число. Повторите ввод")
        return GET_NUMBER_VALUE

    input_number_value = update.message.text
    context.user_data["number_value"] = float(input_number_value)
    await update.message.reply_text(
        """Введите время розыгрыша лота в формате ISO 8601\n"""
        """Например, 2023-01-01 00:00:00 (год-месяц-дата часы:минуты:секунды)""",
        reply_markup=cancel_markup
    )

    return GET_DRAW_TIME


async def draw_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    input_date = update.message.text
    try:
        date = dt.datetime.fromisoformat(input_date)
        if date.tzinfo is None:
            date = date.replace(tzinfo=ZoneInfo("Asia/Yekaterinburg"))

    except ValueError:
        await update.message.reply_text("Некорректно введённая дата. Повторите ввод")
        return GET_DRAW_TIME

    context.user_data["draw_time"] = date
    await update.message.reply_text(
        """Проверьте ещё раз. Всё верно?\n"""
        f"""{context.user_data.items()}""",
        reply_markup=cancel_markup
    )

    return DO_FINAL_CHECK


async def final_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    published_at = update.message.date.astimezone(ZoneInfo("Asia/Yekaterinburg"))
    name, description, image_id = context.user_data["name"], context.user_data["description"], context.user_data[
        "image_id"]
    numbers_count, number_value = context.user_data["numbers_count"], context.user_data["number_value"]
    draw_time = context.user_data["draw_time"]
    is_ok = database.add_lot(name, description, image_id, numbers_count, number_value, published_at, draw_time)
    reply_keyboard = [["Добавить лот"],
                      ["Удалить лот"],
                      ["Объявить розыгрыш"]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    if is_ok:
        await update.message.reply_text(
            """Потрясающе, лот добавлен в базу данных!""",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            """К сожалению, лот не был добавлен в базу данных""",
            reply_markup=reply_markup
        )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    context.user_data.clear()
    await update.message.reply_text(
        "Вы всегда можете начать заново",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def get_add_lot_conversation_handler() -> ConversationHandler:
    message_cancel_filter = filters.Regex("^[Оо]тмена$")
    cancel_filter = message_cancel_filter | filters.COMMAND
    return ConversationHandler(
        entry_points=[CommandHandler("add_lot", start_adding_lot_conversation),
                      MessageHandler(filters.Regex("^(Добавить лот)$"), start_adding_lot_conversation)],
        states={
            GET_NAME: [MessageHandler(filters.TEXT & ~cancel_filter, name)],
            GET_DESCRIPTION: [MessageHandler(filters.TEXT & ~cancel_filter, description)],
            GET_PHOTO: [MessageHandler(filters.PHOTO & ~cancel_filter, photo)],
            GET_NUMBERS_COUNT: [MessageHandler(filters.TEXT & ~cancel_filter, numbers_count)],
            GET_NUMBER_VALUE: [MessageHandler(filters.TEXT & ~cancel_filter, number_value)],
            GET_DRAW_TIME: [MessageHandler(filters.TEXT & ~cancel_filter, draw_time)],
            DO_FINAL_CHECK: [MessageHandler(filters.TEXT & ~cancel_filter, final_check)]
        },
        fallbacks=[MessageHandler(message_cancel_filter, cancel),
                   CommandHandler("cancel", cancel)],
    )
