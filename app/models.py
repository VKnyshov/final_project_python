# from sqlalchemy import Column, Integer, String, DateTime
# from .database import Base
# import datetime
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(255), unique=True, index=True, nullable=False)  # Додаємо довжину 255
#     password = Column(String(255), nullable=False)  # Додаємо довжину 255
#     full_name = Column(String(100), nullable=True)  # Додаємо довжину 100
#     last_login = Column(DateTime, nullable=True)
#     last_logout = Column(DateTime, nullable=True)

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    last_login = Column(DateTime, nullable=True)
    last_logout = Column(DateTime, nullable=True)

    # Зв'язок один-до-багатьох (User → Posts)
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000), nullable=False)  # Текст поста
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Час створення
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # Час оновлення
    user_id = Column(Integer, ForeignKey("users.id"))  # Зв'язок із User

    # Визначаємо зворотний зв'язок із користувачем
    owner = relationship("User", back_populates="posts")
