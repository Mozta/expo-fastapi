from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import settings

password_hash = PasswordHash.recommended()  # Argon2


def hashear_password(password: str) -> str:
    return password_hash.hash(password)

def verificar_password(password: str, hash_guardado: str) -> bool:
    return password_hash.verify(password, hash_guardado)

def crear_token(correo: str, rol: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expira_minutos)
    payload = {"sub": correo, "rol": rol, "exp": expira}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algoritmo)

def decodificar_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algoritmo])
