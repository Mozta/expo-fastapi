from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import buscar_proyecto
from app.repository import repositorio
from app.schemas import Evaluacion, EvaluacionIn, Proyecto

router = APIRouter(prefix="/proyectos/{proyecto_id}/evaluaciones", tags=["Evaluaciones"])

@router.post("", response_model=Evaluacion, status_code=status.HTTP_201_CREATED)
def crear_evaluacion(
    proyecto: Annotated[Proyecto, Depends(buscar_proyecto)],
    datos: EvaluacionIn,
):
    return repositorio.crear_evaluacion(proyecto.id, datos)


@router.get("", response_model=list[Evaluacion])
def listar_evaluaciones(proyecto: Annotated[Proyecto, Depends(buscar_proyecto)]):
    return repositorio.listar_evaluaciones(proyecto.id)
