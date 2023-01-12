from datetime import datetime
from sqlalchemy.orm import sessionmaker
from consts import USER_POST_INTERVAL

class DBWorker:
    def __init__(self):
        # Create a session
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def create_user(self, msg):
        """Creates a new user in the database.

        Args:
            msg (telegram.Message): The message object containing information about the user.

        Returns:
            models.User: The created user object.
        """
        user = User(
            id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name
        )
        self.session.add(user)
        self.session.commit()
        return user

    def make_users_previous_post_archived(self, user: User):
        """Marks the user's previous post as archived.

        Args:
            user (models.User): The user whose previous post should be archived.

        Returns:
            int: The ID of the archived post, or None if no previous post was found.
        """
        post = self.session.query(Post).filter(Post.from_user == user, Post.archived == False).first()
        if post is None:
            return None
        post.archived = True
        self.session.commit()
        return post.msg_id

    def get_user(self, msg):
        """Gets the user object for the given message.

        Args:
            msg (telegram.Message): The message object containing information about the user.

        Returns:
            models.User: The user object, or None if the user does not exist in the database.
        """
        return self.session.query(User).filter_by(id=msg.from_user.id).first()

    def create_post(self, user, msg):
        """Creates a new post in the database.

        Args:
            user (models.User): The user who created the post.
            msg (telegram.Message): The message object containing the post text.

        Returns:
            models.Post: The created post object.
        """
        post = Post(from_user=user, text=msg.text)
        self.session.add(post)
        self.session.commit()
        return post

    def update_post_msg_id(self, post, msg_id):
        """Updates the message ID of the given post.

        Args:
            post (models.Post): The post object to update.
            msg_id (int): The new message ID.
        """
        post.msg_id = msg_id
        self.session.commit()

    def too_often(self, user):
        """Checks if the user has made a post too recently.

        Args:
            user (models.User): The user to check.

        Returns:
            bool: True if the user has made a post within the interval specified in USER_POST_INTERVAL, False otherwise.
        """
        if user.is_admin:
            return False
            post = self.session.query(Post).filter(Post.from_user == user, Post.archived == False).first()
        if post is None:
            return False

        time_delta = (datetime.utcnow() - post.posted_at).total_seconds()
        return time_delta < USER_POST_INTERVAL

