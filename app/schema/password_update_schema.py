from pydantic import BaseModel

class PasswordUpdate(BaseModel):
    password:str

    class Config:
        orm_mode = True