import datetime
from peewee import SqliteDatabase, Model, IntegerField, CharField, FloatField, DateTimeField, TextField, \
    ForeignKeyField, BooleanField

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        db_table = "Users"

    tg_id = IntegerField(unique=True)
    username = CharField(max_length=32, unique=True)
    first_name = CharField(max_length=64, null=True)
    second_name = CharField(max_length=64, null=True)
    access_level = CharField(max_length=32, default="Customer")


class Lot(BaseModel):
    class Meta:
        db_table = "Lots"

    name = CharField(max_length=128)
    description = TextField(null=True)
    numbers_count = IntegerField()
    number_value = FloatField()
    draw_time = DateTimeField(default=datetime.datetime.now)
    published_at = DateTimeField(default=datetime.datetime.now)



class Product(BaseModel):
    class Meta:
        db_table = "Products"

    lot = ForeignKeyField(Lot, unique=True, on_delete="CASCADE")
    number = IntegerField()
    is_bought = BooleanField(default=0)


class Cart(BaseModel):
    class Meta:
        db_table = "Carts"

    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)


if __name__ == "__main__":
    tables = [
        User,
        Cart,
        Lot,
        Product,

    ]
    db.create_tables(tables)
