from peewee import (
    SqliteDatabase, Model, BigIntegerField, CharField,
    IntegerField, DateTimeField, AutoField
)
from datetime import datetime


db = SqliteDatabase('data.db')


class BaseModel(Model):

    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        db_table = 'Users'
        
    id = AutoField()
    telegram_id = BigIntegerField(unique=True)
    name = CharField(max_length=100)
    telegram_name = CharField(max_length=100)


class Request(BaseModel):
    class Meta:
        db_table = 'Requests'

    id = AutoField()
    request = CharField(max_length=1000)
    answer_request = CharField(max_length=1000)
    user_id = IntegerField()
    created_at = DateTimeField(default=datetime.now)


def initialize_db() -> None:
    """Инициализация таблиц, если их еще нет."""
    with db:
        db.create_tables([User, Request], safe=True)