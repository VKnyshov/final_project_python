from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)  # Додаємо довжину
    password = Column(String(255), nullable=False)  # Додаємо довжину
    full_name = Column(String(255), nullable=True)  # Додаємо довжину