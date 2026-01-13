from datetime import datetime, timedelta, timezone
import secrets
from typing import Any
import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Generamos el hash de la contraseña
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verificamos la contraseña ingresada con el hash almacenado
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generamos el token de acceso
def create_access_token(subject: str | Any, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

def decode_token(token:str):
    try:
        playload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        return playload
    except jwt.DecodeError as e:
        raise Exception(f"Token No valido o expiraod {e}")

# ---- reset token utilities ----
def generate_reset_token() -> str:
    # token random, suficientemente largo
    return secrets.token_urlsafe(48)

def get_token_hash(token: str) -> str:
   return pwd_context.hash(token)

def verify_token_hash(token: str, token_hash: str) -> bool:
    return pwd_context.verify(token, token_hash)
