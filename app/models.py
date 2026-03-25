from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

# define DB tables as Python models
class Post(Base):
    __tablename__ = "posts"

    id = Column(type_=Integer, primary_key=True, nullable=False)
    title = Column(type_=String, nullable=False)
    content = Column(type_=String, nullable=False)
    published = Column(type_=Boolean, nullable=False, server_default='TRUE')
    created_at = Column(type_=TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(column="users.id", name="fk_posts_users", ondelete="CASCADE"), nullable=False)

    # Many-To-One
    user = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = "users"

    id = Column(type_=Integer, primary_key=True, nullable=False)
    email = Column(type_=String, nullable=False)
    password = Column(type_=String, nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))    

    # One-To-Many
    posts = relationship("Post", back_populates="user") 

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey(column="users.id", name="fk_votes_users", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(column="posts.id", name="fk_votes_posts", ondelete="CASCADE"), primary_key=True)