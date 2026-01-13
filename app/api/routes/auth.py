from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.password_reset import ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.user import UserLogin
from app.schemas.token import Token
from app.services.auth import email_forgot_password_link, login_access_token, reset_user_password

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, 
                db: Session = Depends(get_db), 
               ):
    """Login de usuario con email y contraseña"""

    return login_access_token(db, user_login.email, user_login.password)

@router.post('/forgot-password')
async def forgot_password(fpIn:ForgotPasswordRequest, bg: BackgroundTasks,
                          db: Session = Depends(get_db)):
    
    await email_forgot_password_link(fpIn, bg, db)

    return JSONResponse ({"msg":"Se envió el correo para restablecer la contraseña"})  
    

@router.post('/reset-password')
async def reset_password(rpIn: ResetPasswordRequest, db: Session = Depends(get_db)):

    await reset_user_password(rpIn, db)
    return JSONResponse({"msg":"Contraseña restablecida con éxito"})
