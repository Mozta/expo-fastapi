from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, func, select

from app.errors import Conflicto
from app.models import EvaluacionDB, ProyectoDB, UsuarioDB
from app.schemas import Categoria, EvaluacionIn, ProyectoIn, Resumen, UsuarioIn
from app.security import hashear_password


class RepositorySQL:
    def __init__(self, session: Session) -> None:
        self.session = session

    def crear_usuario(self, datos: UsuarioIn) -> UsuarioDB:
        usuario = UsuarioDB(
            correo=datos.correo,
            nombre=datos.nombre,
            password_hash=hashear_password(datos.password),
        )
        self.session.add(usuario)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise Conflicto(f"Ya existe un usuario con el correo: {datos.correo}")
        self.session.refresh(usuario)
        return usuario

    def obtener_usuario_por_correo(self, correo: str) -> UsuarioDB | None:
        return self.session.exec(select(UsuarioDB).where(UsuarioDB.correo == correo)).first()


    # Proyectos
    def crear_proyecto(self, datos: ProyectoIn) -> ProyectoDB:
        proyecto = ProyectoDB(**datos.model_dump())
        self.session.add(proyecto)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise Conflicto(f"Ya existe un proyecto llamado '{datos.nombre}'")
        self.session.refresh(proyecto)
        return proyecto

    def listar_proyectos(self, categoria: Categoria | None, limite: int) -> list[ProyectoDB]:
        consulta = select(ProyectoDB)
        if categoria is not None:
            consulta = consulta.where(ProyectoDB.categoria == categoria)
        consulta = consulta.order_by(ProyectoDB.id).limit(limite)
        return list(self.session.exec(consulta).all())

    def obtener_proyecto(self, proyecto_id: int) -> ProyectoDB | None:
        return self.session.get(ProyectoDB, proyecto_id)

    # Evaluaciones
    def crear_evaluacion(self, proyecto_id: int, datos: EvaluacionIn) -> EvaluacionDB:
        evaluacion = EvaluacionDB(proyecto_id=proyecto_id, **datos.model_dump())
        self.session.add(evaluacion)
        self.session.commit()
        self.session.refresh(evaluacion)
        return evaluacion

    def listar_evaluaciones(self, proyecto_id: int) -> list[EvaluacionDB]:
        consulta = select(EvaluacionDB).where(EvaluacionDB.proyecto_id == proyecto_id)
        return list(self.session.exec(consulta).all())

    def resumen(self, proyecto_id: int) -> Resumen:
        consulta = select(
            func.count(EvaluacionDB.id),
            func.avg(EvaluacionDB.innovacion),
            func.avg(EvaluacionDB.viabilidad),
            func.avg(EvaluacionDB.presentacion),
        ).where(EvaluacionDB.proyecto_id == proyecto_id)
        total, innovacion, viabilidad, presentacion = self.session.exec(consulta).one()

        if total == 0:
            return Resumen(
                proyecto_id=proyecto_id, total_evaluaciones=0,
                innovacion=None, viabilidad=None, presentacion=None, general=None,
            )

        innovacion, viabilidad, presentacion = float(innovacion), float(viabilidad), float(presentacion)
        general = (innovacion + viabilidad + presentacion) / 3
        return Resumen(
            proyecto_id=proyecto_id,
            total_evaluaciones=total,
            innovacion=round(innovacion, 2),
            viabilidad=round(viabilidad, 2),
            presentacion=round(presentacion, 2),
            general=round(general, 2),
        )