import aiosmtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

async def send_email(to_email: str, subject: str, content: str):
    if not FROM_EMAIL:
        raise RuntimeError("FROM_EMAIL não configurado nas variáveis de ambiente.")
    if not to_email or not subject or not content:
        raise ValueError("Parâmetros obrigatórios ausentes para envio de e-mail.")

    message = EmailMessage()
    message["From"] = FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD
        )
    except Exception as e:
        logger.error(f"Erro ao enviar email: {e}")
        raise RuntimeError("Falha ao enviar o email") from e