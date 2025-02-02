from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserUpdate(BaseModel):
    """Схема для оновлення користувача"""
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
