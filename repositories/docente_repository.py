from typing import Optional
from sqlalchemy.orm import Session
from database.models import Docente
from repositories.base_repository import BaseRepository


class DocenteRepository(BaseRepository[Docente]):

    def __init__(self, session: Session):
        super().__init__(session, Docente)

    def obtener_por_cedula(self, cedula: str) -> Optional[Docente]:
        return (
            self.session.query(Docente)
            .filter(Docente.cedula == cedula)
            .first()
        )

    def obtener_con_asignaturas(self) -> list[Docente]:
        """Retorna todos los docentes con sus asignaturas precargadas."""
        from sqlalchemy.orm import joinedload
        return (
            self.session.query(Docente)
            .options(joinedload(Docente.asignaturas))
            .order_by(Docente.apellidos)
            .all()
        )
