from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    id: int
    email: EmailStr
    password: str