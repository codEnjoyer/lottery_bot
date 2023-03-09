from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from models import User

from logging import getLogger

logger = getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = [768519797]
    user = update.effective_user
    id, username, first_name, second_name = user.id, user.username, user.first_name, user.last_name
    access_level = "Admin" if id in admins else "Customer"

    logger.info(f"Пользователь {first_name} ({id=}) начал диалог с ботом.")

    custom_user = User.create(tg_id=id, username=username, first_name=first_name, second_name=second_name,
                              access_level=access_level)

    reply_keyboard = [["/lots"],
                      ["/cart", "/help"]]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=False, input_field_placeholder="У меня есть много интересного :)"
    )

    await update.message.reply_html(f"Привет, {user.mention_html()}, рад тебя видеть!\n"
                                    f"Это лотерейный бот. При помощи него ты можешь испытать удачу и попытаться "
                                    f"выиграть хорошие призы за низкую цену!",
                                    reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id={user.id}) узнал правила общения с ботом.")
    await update.message.reply_text("Плати и выигрывай!")
