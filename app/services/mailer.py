from fastapi_mail import FastMail, ConnectionConfig,MessageSchema
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME = settings.SMTP_USER,
    MAIL_PASSWORD = settings.SMTP_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM or "noreply@example.com",
    MAIL_SERVER = settings.SMTP_HOST,
    MAIL_PORT = settings.SMTP_PORT,
    MAIL_STARTTLS = True,  # QQ邮箱使用STARTTLS
    MAIL_SSL_TLS = False,   # 不使用SSL/TLS
    USE_CREDENTIALS = True,
)

fm =FastMail(conf)

async def send_email(to:str,subject:str,html:str):
    msg = MessageSchema(subject = subject, recipients = [to],body = html,subtype = "html")
    await fm.send_message(msg)