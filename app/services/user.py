from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash


def create_user_account(db:Session, user_in: UserCreate) -> User:
        """Registrar un nuevo usuario"""
        # Verificar si el usuario ya existe
        existing_user = get_user_by_email(db, user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear el nuevo usuario
        new_user = create(db, user_in)
        return new_user
    
def create(db: Session, user_in: UserCreate) -> User:
        """Crear un nuevo usuario"""
        print("Creating user:", user_in, user_in.password)
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            name=user_in.name,
            last_name=user_in.last_name,
            hashPassword=hashed_password,
            isActive=user_in.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
def get_user_by_email(db: Session, email: str) -> User:
        """Obtener usuario por email"""
        user = db.query(User).filter(User.email == email).first()
        return user
    
def get_user_by_id(db: Session, user_id: int) -> User:
        """Obtener usuario por ID"""
        user = db.query(User).filter(User.id == user_id).first()
        return user

async def change_user_password(db: Session, user: User, user_data):
        from app.core.security import verify_password, get_password_hash
        if not verify_password(user_data.old_password, user.hashPassword):
               raise HTTPException(status_code=400, detail="La contraseña antigua es incorrecta.")
        user.hashPassword = get_password_hash(user_data.new_password)

        db.add(user)
        db.commit()

