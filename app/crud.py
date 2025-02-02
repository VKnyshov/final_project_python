from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas

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

def get_user_by_id(db: Session, user_id: int):
    """Пошук користувача за ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def filter_users(db: Session, user_id: int = None, email: str = None, full_name: str = None, last_login: str = None):
    """Фільтрація користувачів за вказаними параметрами"""
    query = db.query(models.User)

    if user_id:
        query = query.filter(models.User.id == user_id)
    if email:
        query = query.filter(models.User.email.ilike(f"%{email}%"))  # Пошук часткового збігу email
    if full_name:
        query = query.filter(models.User.full_name.ilike(f"%{full_name}%"))  # Пошук часткового збігу full_name
    if last_login:
        query = query.filter(models.User.last_login >= last_login)  # Фільтр по останньому входу (>=)

    return query.all()

from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_posts_by_user(db: Session, user_id: int):
    """Отримання всіх постів користувача"""
    return db.query(models.Post).filter(models.Post.user_id == user_id).all()
# .......................................................................

def create_post(db: Session, user: models.User, post_data: schemas.PostCreate):
    """Створення нового поста для авторизованого користувача"""
    new_post = models.Post(
        text=post_data.text,
        user_id=user.id  # Прив'язуємо пост до ID користувача
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def delete_post(db: Session, user: models.User, post_id: int):
    """Видалення поста (тільки власник може видалити свій пост)"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Пост не знайдено")

    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Ви не можете видалити чужий пост")

    db.delete(post)
    db.commit()
    return {"message": "Пост успішно видалено"}
