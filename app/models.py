from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text

# define DB tables as Python models
class Post(Base):
    __tablename__ = "posts"

    id = Column(type_=Integer, primary_key=True, nullable=False)
    title = Column(type_=String, nullable=False)
    content = Column(type_=String, nullable=False)
    published = Column(type_=Boolean, nullable=False, server_default='TRUE')
    rating = Column(type_=Integer, nullable=True)
    created_at = Column(type_=TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"

    id = Column(type_=Integer, primary_key=True, nullable=False)
    email = Column(type_=String, nullable=False)
    password = Column(type_=String, nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))         