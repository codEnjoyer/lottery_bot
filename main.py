# region VersionCheck
from telegram import __version__ as tg_version

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {tg_version}. To view the "
        f"{tg_version} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{tg_version}/examples.html"
    )
# endregion


import logging
from telegram.ext import ApplicationBuilder

from config import load_config
from handlers import get_commands_handlers, get_conversations_handlers, get_messages_handlers

logging.basicConfig(
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
config = load_config(".env")


def main():
    application = ApplicationBuilder().token(config.tg_bot.token).build()
    handlers = [
        *get_commands_handlers(),
        *get_conversations_handlers(),
        *get_messages_handlers(),
    ]

    application.add_handlers(handlers)
    logger.info("Обработчики зарегистрированы")
    try:
        logger.info("Бот запущен")
        application.run_polling()
    except (SystemExit, KeyboardInterrupt):
        logger.error("Бот остановлен!")


if __name__ == '__main__':
    main()
