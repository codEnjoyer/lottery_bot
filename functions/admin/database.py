from peewee import IntegrityError, ModelDictCursorWrapper

from models import Lot
import datetime as dt
import logging

logger = logging.getLogger(__name__)


def add_lot(name: str, description: str, numbers_count: int, number_value: float, published_at: dt.datetime,
            draw_time: dt.datetime):
    lot = Lot(name=name, description=description, numbers_count=numbers_count, number_value=number_value,
              published_at=published_at, draw_time=draw_time)
    try:
        logger.info(f"""Лот "{name}" добавляется в базу данных""")
        lot.save()
    except IntegrityError:
        logger.info(f"""Не удалось добавить {name} в базу данных""")


def get_all_lots() -> ModelDictCursorWrapper:
    return Lot.select().dicts().execute()


def delete_lot(id: int) -> bool:
    try:
        Lot[id].delete_instance()
        return True
    except Exception as e:
        logger.error(e)
        return False
