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
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: str
    mail_server: str
    mail_from_name: str

    class Config:
        env_file = ".env"


settings = Settings()
