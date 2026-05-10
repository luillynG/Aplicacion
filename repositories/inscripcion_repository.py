from typing import Optional
from sqlalchemy.orm import Session
from database.models import Inscripcion
from repositories.base_repository import BaseRepository


class InscripcionRepository(BaseRepository[Inscripcion]):

    def __init__(self, session: Session):
        super().__init__(session, Inscripcion)

    def obtener_por_estudiante_y_periodo(
        self, id_estudiante: int, periodo_escolar: str
    ) -> Optional[Inscripcion]:
        """Verifica si un estudiante ya está inscrito en un período."""
        from database.models import AñoSeccion
        return (
            self.session.query(Inscripcion)
            .join(AñoSeccion, AñoSeccion.id_seccion == Inscripcion.id_seccion)
            .filter(
                Inscripcion.id_estudiante      == id_estudiante,
                AñoSeccion.periodo_escolar     == periodo_escolar,
            )
            .first()
        )

    def obtener_por_seccion(self, id_seccion: int) -> list[Inscripcion]:
        """Retorna todas las inscripciones de una sección."""
        return (
            self.session.query(Inscripcion)
            .filter(Inscripcion.id_seccion == id_seccion)
            .all()
        )
