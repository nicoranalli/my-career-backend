from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.password_reset import ChangePasswordRequest
from app.schemas.user import UserCreate, UserOut
from app.services.user import change_user_password, create_user_account
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["users"])


@router.post('/signup', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):

    new_user = create_user_account(db, user_in)

    return new_user

@router.post('/change-password', status_code=status.HTTP_200_OK)
async def change_password(chP: ChangePasswordRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if chP.new_password != chP.confirm_new_password:
        raise HTTPException(status_code=400, detail="Las nuevas contraseñas no coinciden.")

    if not current_user or not current_user.isActive:
        raise HTTPException(status_code=400, detail="Usuario inválido o inactivo.")

    await change_user_password(db, current_user, chP)

    return JSONResponse({"msg":"Contraseña cambiada con éxito"})
    

@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user