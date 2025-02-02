from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, database, crud, auth
from typing import List

app = FastAPI()


# Створюємо таблиці при старті сервера
@app.on_event("startup")
def startup():
    print("✅ Перевіряємо, чи створені таблиці...")
    models.Base.metadata.create_all(bind=database.engine)


# ✅ Реєстрація користувача
@app.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


# ✅ Логін користувача
@app.post("/login/", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user.email})

    # Оновлюємо час входу
    crud.update_last_login(db, user)

    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Видалення користувача
@app.delete("/users/me/", status_code=204)
def delete_current_user(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}


# ✅ Оновлення користувача
@app.put("/users/me/", response_model=schemas.UserResponse)
def update_current_user(
        user_update: schemas.UserUpdate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user),
):
    updated_user = crud.update_user(db, current_user, user_update)
    return updated_user


# ✅ Вихід користувача (оновлення last_logout)
@app.post("/logout/", status_code=200)
def logout_user(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    crud.update_last_logout(db, current_user)
    return {"message": "Logout successful"}


# ✅ Отримання всіх користувачів (авторизовані)
@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_all_users(db)


# ✅ Пошук користувача за ID або Email
@app.get("/users/search/", response_model=schemas.UserResponse)
def search_user(
        user_id: int = None,
        email: str = None,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    if user_id:
        user = crud.get_user_by_id(db, user_id)
    elif email:
        user = crud.get_user_by_email(db, email)
    else:
        raise HTTPException(status_code=400, detail="Необхідно вказати або ID, або Email")

    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    return user


# ✅ Фільтрація користувачів
@app.get("/users/filter/", response_model=List[schemas.UserResponse])
def filter_users(
        user_id: int = None,
        email: str = None,
        full_name: str = None,
        last_login: str = None,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    users = crud.filter_users(db, user_id, email, full_name, last_login)

    if not users:
        raise HTTPException(status_code=404, detail="Користувачів не знайдено")

    return users


# ✅ Отримання постів користувача (неавторизовані)
@app.get("/users/{user_id}/posts/", response_model=list[schemas.PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(database.get_db)):
    posts = crud.get_posts_by_user(db, user_id)
    if not posts:
        raise HTTPException(status_code=404, detail="Користувач не має постів")
    return posts


@app.post("/posts/", response_model=schemas.PostResponse)
def create_post(
        post_data: schemas.PostCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)  # Авторизація
):
    """Створення поста (тільки для авторизованих)"""
    return crud.create_post(db, current_user, post_data)


@app.delete("/posts/{post_id}/")
def delete_post(
        post_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)  # Авторизація
):
    """Видалення поста (тільки для власника)"""
    return crud.delete_post(db, current_user, post_id)


@app.put("/posts/{post_id}/", response_model=schemas.PostResponse)
def edit_post(
        post_id: int,
        post_update: schemas.PostUpdate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user),
):
    """Редагування поста (може редагувати лише власник)"""
    return crud.update_post(db, current_user, post_id, post_update)
