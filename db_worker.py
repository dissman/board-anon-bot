import datetime

from peewee import DoesNotExist

from consts import USER_POST_INTERVAL
from models import User, Post


class DBWorker:
    def __init__(self, db):
        self.db = db

    def create_user(self, msg):
        """Creates a new user in the database.

        Args:
            msg (telegram.Message): The message object containing information about the user.

        Returns:
            models.User: The created user object.
        """
        return User.create(
            id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name
        )

    def make_users_previous_post_archived(self, user: User):
        """Marks the user's previous post as archived.

        Args:
            user (models.User): The user whose previous post should be archived.

        Returns:
            int: The ID of the archived post, or None if no previous post was found.
        """
        try:
            old_post = Post.get((Post.from_user == user) & (Post.archived == False))
        except Exception:  # for now...
            return None

        old_post.archived = True
        old_post.save()
        return old_post.msg_id

    def get_user(self, msg):
        """Gets the user object for the given message.

        Args:
            msg (telegram.Message): The message object containing information about the user.

        Returns:
            models.User: The user object, or None if the user does not exist in the database.
        """
        try:
            return User.get(User.id == msg.from_user.id)
        except DoesNotExist:
            return None

    def create_post(self, user, msg):
        """Creates a new post in the database.

        Args:
            user (models.User): The user who created the post.
            msg (telegram.Message): The message object containing the post text.

        Returns:
            models.Post: The created post object.
        """
        p = Post.create(from_user=user, text=msg.text)
        p.save()
        return p

    def update_post_msg_id(self, post, msg_id):
        """Updates the message ID of the given post.

        Args:
            post (models.Post): The post object to update.
            msg_id (int): The new message ID.
        """
        post.msg_id = msg_id
        post.save()

    def too_often(self, user):
        """Checks if the user has made a post too recently.

        Args:
            user (models.User): The user to check.

        Returns:
            bool: True if the user has made a post within the interval specified in USER_POST_INTERVAL, False otherwise.
        """
        if user.is_admin:
            return False

        try:
            old_post = Post.get((Post.from_user == user) & (Post.archived == False))
        except DoesNotExist:
            return False

        time_delta = (datetime.datetime.utcnow() - old_post.posted_at).total_seconds()
        return time_delta < USER_POST_INTERVAL
