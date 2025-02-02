from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    """Пошук користувача за email"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Реєстрація нового користувача"""
    hashed_password = pwd_context.hash(user.password)  # Хешуємо пароль
    db_user = models.User(
        email=user.email,
        password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: models.User, user_update: schemas.UserUpdate):
    """Оновлення користувача (тільки full_name та password)"""
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.password is not None:
        user.password = pwd_context.hash(user_update.password)

    db.commit()
    db.refresh(user)
    return user

def update_last_login(db: Session, user: models.User):
    """Оновлення часу входу користувача"""
    user.last_login = datetime.utcnow()
    db.commit()

def update_last_logout(db: Session, user: models.User):
    """Оновлення часу виходу користувача"""
    user.last_logout = datetime.utcnow()
    db.commit()

def get_all_users(db: Session):
    """Отримати всіх користувачів"""
    return db.query(models.User).all()

# ...............................................................................
def get_user_by_id(db: Session, user_id: int):
    """Пошук користувача за ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

