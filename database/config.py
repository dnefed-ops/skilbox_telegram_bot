from peewee import *


db = SqliteDatabase('data.db')

class BaseModel(Model):

    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        db_table = 'Users'

    telegram_id = BigIntegerField(unique=True)
    name = CharField(max_length=100)
    telegram_name = CharField(max_length=100)


class Request(BaseModel):
    class Meta:
        db_table = 'Requests'

    request = CharField(max_length=1000)
    answer_request = CharField(max_length=1000)
    user_id = IntegerField