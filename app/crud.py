from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

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
        user.password = pwd_context.hash(user_update.password)  # Хешуємо пароль перед збереженням

    db.commit()
    db.refresh(user)
    return user
