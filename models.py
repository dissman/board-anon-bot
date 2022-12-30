import datetime

from peewee import *

# db = SqliteDatabase('anon.sqlite')
db = MySQLDatabase(
    'anon-board',
    user='root',
    password='',
    host='localhost',
    port=3306
)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    """A model representing a user.

    Attributes:
        id (char): The user's ID.
        username (char): The user's username.
        first_name (char): The user's first name.
        last_name (char): The user's last name.
        blocked (bool): Whether the user is blocked.
        is_admin (bool): Whether the user is an admin.
    """
    id = CharField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    blocked = BooleanField(default=False)
    is_admin = BooleanField(default=False)


class Post(BaseModel):
    """A model representing a post.

    Attributes:
        from_user (User): The user who made the post.
        text (char): The text of the post.
        posted_at (datetime): The time the post was made.
        msg_id (int): The ID of the message containing the post.
        archived (bool): Whether the post is archived.
    """
    from_user = ForeignKeyField(User, on_delete='SET NULL', null=True)
    text = CharField(max_length=300)
    posted_at = DateTimeField(default=datetime.datetime.utcnow)
    msg_id = BigIntegerField(null=True)
    archived = BooleanField(default=False)
