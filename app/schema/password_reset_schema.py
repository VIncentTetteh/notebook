from pydantic import BaseModel, EmailStr

class PasswordReset(BaseModel):
    email:EmailStr

    class Config:
        orm_mode = True