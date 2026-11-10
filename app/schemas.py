from enum import Enum
from pydantic import BaseModel, Field

class Categoria(str, Enum):
    software = "Software"
    hardware = "Hardware"
    impacto_social = "Impacto social"
    ia = "Inteligencia Artificial"

class ProyectoIn(BaseModel):
    nombre: str = Field(min_length=3, max_length=120)
    equipo: list[str] = Field(min_length=1, max_length=5)
    categoria: Categoria

class Proyecto(ProyectoIn):
    id: int

class EvaluacionIn(BaseModel):
    evaluador: str = Field(min_length=3, max_length=80)
    innovacion: int = Field(ge=0, le=10)
    viabilidad: int = Field(ge=0, le=10)
    presentacion: int = Field(ge=0, le=10)
    comentario: str | None = Field(default=None, max_length=500)

class Evaluacion(EvaluacionIn):
    id: int
    proyecto_id: int

class Resumen(BaseModel):
    proyecto_id: int
    total_evaluaciones: int
    innovacion: float | None
    viabilidad: float | None
    presentacion: float | None
    general: float | None