from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    database_host: str = os.getenv('DATABASE_HOST')
    database_name: str = os.getenv('DATABASE_NAME')
    database_username: str = os.getenv('DATABASE_USERNAME')
    database_password: str = os.getenv('DATABASE_PASSWORD')
    database_port: str = os.getenv('DATABASE_PORT')
    algorithm: str = os.getenv('ALGORITH')
    secret_key: str = os.getenv('SECRET_KEY')
    access_token_expire_minutes: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    mail_username: str = os.getenv('MAIL_USERNAME')
    mail_password: str = os.getenv('MAIL_PASSWORD')
    mail_from: str = os.getenv('MAIL_FROM')
    mail_port: str = os.getenv('MAIL_PORT')
    mail_server: str = os.getenv('MAIL_SERVER')
    mail_from_name: str = os.getenv('MAIL_FROM_NAME')


settings = Settings()
