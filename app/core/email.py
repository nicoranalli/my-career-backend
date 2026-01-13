import os
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi.background import BackgroundTasks
from app.core.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME = "nicoranalli9@gmail.com",
    MAIL_PASSWORD = settings.MAIL_APP_PASSWORD,
    MAIL_FROM = "nicoranalli9@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER ="smtp.gmail.com",
    MAIL_FROM_NAME="Reseteo de contraseña MyCareer",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False
)

fm = FastMail(conf)


async def send_email(recipients: list, subject: str, body_html: str,
                     background_tasks: BackgroundTasks):
    print("Comenzando a enviar el correo a %s con el asunto %s", recipients, subject)

    try:
        # Crea el mensaje
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body_html,
            subtype="html"  # Puedes ajustar el tipo si no es HTML
        )
        print("Mensaje creado correctamente, enviando ahora...")

        # Enviar el correo en segundo plano
        background_tasks.add_task(fm.send_message, message)
        print("Correo enviado exitosamente a %s", recipients)
    except Exception as e:
        print("Error al enviar el correo: %s", str(e))