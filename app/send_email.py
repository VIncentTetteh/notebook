from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from .schemas import EmailSchema
from .config import settings

BASE_DIR = Path(__file__).resolve().parent

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, 'templates')
)


async def send_registration_mail(subject: str, email_to: EmailSchema, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message, template_name="email.html")
