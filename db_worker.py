import datetime

from peewee import DoesNotExist

from consts import USER_POST_INTERVAL
from models import User, Post


class DBWorker:
    def __init__(self, db):
        self.db = db

    def create_user(self, msg):
        return User.create(id=msg.from_user.id,
                           username=msg.from_user.username,
                           first_name=msg.from_user.first_name,
                           last_name=msg.from_user.last_name)

    def make_users_previous_post_archived(self, user: User):
        try:
            old_post = Post.get((Post.from_user == user) &
                                (Post.archived == False))
        except Exception:  # for now...
            return None
        old_post.archived = True
        old_post.save()
        return old_post.msg_id

    def get_user(self, msg):
        try:
            return User.get(User.id == msg.from_user.id)
        except DoesNotExist:
            return None

    def create_post(self, user, msg):
        p = Post.create(from_user=user, text=msg.text)
        p.save()
        return p

    def update_post_msg_id(self, post, msg_id):
        post.msg_id = msg_id
        post.save()

    def too_often(self, user):
        if user.is_admin:
            return False
        try:
            old_post = Post.get((Post.from_user == user) &
                                (Post.archived == False))
        except DoesNotExist:
            return False
        time_delta = (datetime.datetime.utcnow() - old_post.posted_at).total_seconds()
        return time_delta < USER_POST_INTERVAL
