from sqlalchemy.orm import Session

from app.core.email import send_email
from fastapi import BackgroundTasks
from app.core.security import generate_reset_token, get_token_hash
from datetime import datetime, timedelta, timezone
from app.models.user import User
from app.core.config import settings


async def send_password_reset_email(user: User, bg: BackgroundTasks, db:Session):
        
    token = generate_reset_token()
    hashed_token = get_token_hash(token)
    token_expires = datetime.now(timezone.utc) + timedelta(hours=1)


    user.hashedResetToken = hashed_token
    user.hashedResetTokenExpiry = token_expires

    db.add(user)
    db.commit()

    reset_front_link = f"{settings.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"

    html = f"""
    <p>Hola {user.name},</p>
    <p>Para resetear tu contraseña entrá al siguiente link:</p>
    <a href="{reset_front_link}">{reset_front_link}</a>
    <p>Vence en 15 minutos.</p>
    """

    await send_email(
        recipients=[user.email],
        subject="Restablecimiento de contraseña",
        body_html=html,
        background_tasks=bg
    )


   