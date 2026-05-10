from datetime import date
from sqlalchemy.orm import Session
from database.models import Asistencia
from repositories.base_repository import BaseRepository


class AsistenciaRepository(BaseRepository[Asistencia]):

    def __init__(self, session: Session):
        super().__init__(session, Asistencia)

    def obtener_por_inscripcion(self, id_inscripcion: int) -> list[Asistencia]:
        """Retorna todo el historial de asistencia de un estudiante inscrito."""
        return (
            self.session.query(Asistencia)
            .filter(Asistencia.id_inscripcion == id_inscripcion)
            .order_by(Asistencia.fecha)
            .all()
        )

    def obtener_por_fecha_y_seccion(
        self, fecha: date, id_seccion: int
    ) -> list[Asistencia]:
        """Retorna la asistencia de toda una sección en una fecha específica."""
        from database.models import Inscripcion
        return (
            self.session.query(Asistencia)
            .join(Inscripcion, Inscripcion.id_inscripcion == Asistencia.id_inscripcion)
            .filter(
                Asistencia.fecha          == fecha,
                Inscripcion.id_seccion    == id_seccion,
            )
            .all()
        )

    def ya_registrada(self, id_inscripcion: int, fecha: date) -> bool:
        """Verifica si ya existe un registro de asistencia para ese día."""
        return (
            self.session.query(Asistencia)
            .filter(
                Asistencia.id_inscripcion == id_inscripcion,
                Asistencia.fecha          == fecha,
            )
            .first()
        ) is not None
