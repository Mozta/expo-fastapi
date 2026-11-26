import jwt
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import SessionDep
from app.models import ProyectoDB, UsuarioDB
from app.schemas import Rol
from app.security import decodificar_token
from app.repository_sql import RepositorySQL


def get_repositorio(session: SessionDep) -> RepositorySQL:
    return RepositorySQL(session)


RepositorioDep = Annotated[RepositorySQL, Depends(get_repositorio)]


def buscar_proyecto(proyecto_id: int, repositorio: RepositorioDep) -> ProyectoDB:
    proyecto = repositorio.obtener_proyecto(proyecto_id)
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


ProyectoDep = Annotated[ProyectoDB, Depends(buscar_proyecto)]

# Autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_usuario_actual(
        token: Annotated[str, Depends(oauth2_scheme)], repositorio: RepositorioDep
) -> UsuarioDB:
    credenciales_invalidas = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas o token expirado",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = decodificar_token(token)
    except jwt.InvalidTokenError:
        raise credenciales_invalidas

    usuario = repositorio.obtener_usuario_por_correo(payload.get("sub", ""))
    if usuario is None:
        raise credenciales_invalidas

    return usuario

UsuarioActualDep = Annotated[UsuarioDB, Depends(get_usuario_actual)]