import datetime

from peewee import *

# db = SqliteDatabase('anon.sqlite')
db = MySQLDatabase('anon-board', user='root', password='',
                   host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = CharField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    blocked = BooleanField(default=False)
    is_admin = BooleanField(default=False)


class Post(BaseModel):
    from_user = ForeignKeyField(User, on_delete='SET NULL')
    text = CharField(max_length=300)
    posted_at = DateTimeField(default=datetime.datetime.utcnow)
    msg_id = BigIntegerField(null=True)
    archived = BooleanField(default=False)
