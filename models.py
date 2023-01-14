from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Connect to the database
engine = create_engine('sqlite:///database.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(String(20), primary_key=True)
    username = Column(String(20), nullable=True)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    blocked = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

class Post(Base):
    __tablename__ = 'post'
    from_user_id = Column(String(20), ForeignKey('user.id'), nullable=True)
    text = Column(String(300))
    posted_at = Column(DateTime, default=datetime.utcnow, primary_key=True)
    msg_id = Column(Integer, nullable=True)
    archived = Column(Boolean, default=False)
    from_user = relationship("User", foreign_keys=[from_user_id])

# Create the database
Base.metadata.create_all(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
