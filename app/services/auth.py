from fastapi import BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.schemas.password_reset import ForgotPasswordRequest, ResetPasswordRequest
from app.services.email import send_password_reset_email
from app.services.user import get_user_by_email
from app.schemas.token import Token
from app.core.config import settings
from app.core.security import verify_token_hash, verify_password, create_access_token, get_password_hash



def login_access_token(db: Session, email: str, password: str) -> Token:
        user = get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashPassword):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
            )
        if not user.isActive:
            raise HTTPException(status_code=400, detail="Usuario inactivo")

        token = create_access_token(subject=user.email, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return Token(access_token=token, token_type="bearer")
        

async def email_forgot_password_link(fpIn:ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session):
    user = get_user_by_email(db, fpIn.email)
    
    if not user or not user.isActive:
        raise HTTPException(status_code=400, detail="Usuario inválido o inactivo")
    await send_password_reset_email(user, background_tasks, db)

async def reset_user_password(rpIn: ResetPasswordRequest, db: Session):
    user = get_user_by_email(db, rpIn.email)

    if not user or not user.isActive:
            raise HTTPException(status_code=400, detail="Usuario inválido o inactivo.")
    if not user.hashedResetToken or user.hashedResetTokenExpiry < datetime.now():
            raise HTTPException(status_code=400, detail="Token inválido o expirado.")
    
    token_valid = verify_token_hash(rpIn.token, user.hashedResetToken)

    if not token_valid:
            raise HTTPException(status_code=400, detail="Token inválido.")
    user.hashPassword = get_password_hash(rpIn.new_password)
    user.hashedResetToken = None
    user.hashedResetTokenExpiry = None
    
    db.add(user)
    db.commit()


    