from sqlalchemy.orm import Session
from database.models import Asignatura
from repositories.base_repository import BaseRepository


class AsignaturaRepository(BaseRepository[Asignatura]):

    def __init__(self, session: Session):
        super().__init__(session, Asignatura)

    def obtener_por_docente(self, id_docente: int) -> list[Asignatura]:
        """Retorna todas las asignaturas asignadas a un docente específico."""
        from database.models import AsignaturaDocente
        return (
            self.session.query(Asignatura)
            .join(AsignaturaDocente,
                  AsignaturaDocente.id_asignatura == Asignatura.id_asignatura)
            .filter(AsignaturaDocente.id_docente == id_docente)
            .all()
        )
