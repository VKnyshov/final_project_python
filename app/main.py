from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, database, crud, auth

app = FastAPI()

# Створюємо таблиці при старті сервера
@app.on_event("startup")
def startup():
    print("✅ Перевіряємо, чи створені таблиці...")
    models.Base.metadata.create_all(bind=database.engine)

@app.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db, user)

@app.post("/login/", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user.email})

    # Оновлюємо час входу
    crud.update_last_login(db, user)

    return {"access_token": access_token, "token_type": "bearer"}

@app.delete("/users/me/", status_code=204)
def delete_current_user(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.put("/users/me/", response_model=schemas.UserResponse)
def update_current_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Оновлення поточного користувача"""
    updated_user = crud.update_user(db, current_user, user_update)
    return updated_user

@app.post("/logout/", status_code=200)
def logout_user(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Фіксуємо вихід користувача"""
    crud.update_last_logout(db, current_user)
    return {"message": "Logout successful"}


# .................................................................................
@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)  # Авторизація
):
    """Отримання списку всіх користувачів (доступно тільки авторизованим)"""
    return crud.get_all_users(db)
