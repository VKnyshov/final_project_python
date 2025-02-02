from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)  # Додаємо довжину 255
    password = Column(String(255), nullable=False)  # Додаємо довжину 255
    full_name = Column(String(100), nullable=True)  # Додаємо довжину 100
    last_login = Column(DateTime, nullable=True)
    last_logout = Column(DateTime, nullable=True)
