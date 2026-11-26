from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from app.schemas import Categoria, Rol

class UsuarioDB(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    correo: str = Field(max_length=120, unique=True, index=True)
    nombre: str = Field(max_length=80)
    password_hash: str
    rol: Rol = Field(default=Rol.evaluador)
    
class ProyectoDB(SQLModel, table=True):
    __tablename__ = "proyectos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=120, unique=True, index=True)
    equipo: list[str] = Field(sa_column=Column(JSON, nullable=False))
    categoria: Categoria

    evaluaciones: list["EvaluacionDB"] = Relationship(
        back_populates="proyecto", cascade_delete=True
    )


class EvaluacionDB(SQLModel, table=True):
    __tablename__ = "evaluaciones"

    id: int | None = Field(default=None, primary_key=True)
    proyecto_id: int = Field(foreign_key="proyectos.id", index=True, ondelete="CASCADE")
    evaluador: str = Field(max_length=80)
    innovacion: int
    viabilidad: int
    presentacion: int
    comentario: str | None = Field(default=None, max_length=500)

    proyecto: ProyectoDB | None = Relationship(back_populates="evaluaciones")
    