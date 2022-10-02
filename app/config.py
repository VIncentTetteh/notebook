from hashlib import algorithms_available
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_host: str
    database_name: str
    database_username: str
    database_password: str
    database_port: str
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()