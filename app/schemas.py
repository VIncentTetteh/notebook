from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    id: int
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class EmailSchema(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    email:EmailStr

    class Config:
        orm_mode = True

class PasswordUpdate(BaseModel):
    password:str

    class Config:
        orm_mode = True
