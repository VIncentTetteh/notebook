from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    profile_picture:Optional[str] = ""

    class Config:
        orm_mode = True