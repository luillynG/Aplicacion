from sqlalchemy.orm import Session
from database.models import Calificacion
from repositories.base_repository import BaseRepository


class CalificacionRepository(BaseRepository[Calificacion]):

    def __init__(self, session: Session):
        super().__init__(session, Calificacion)

    def obtener_por_inscripcion_y_asignatura(
        self, id_inscripcion: int, id_asignatura: int
    ) -> list[Calificacion]:
        """Retorna todas las notas de un estudiante en una asignatura."""
        return (
            self.session.query(Calificacion)
            .filter(
                Calificacion.id_inscripcion == id_inscripcion,
                Calificacion.id_asignatura  == id_asignatura,
            )
            .order_by(Calificacion.momento, Calificacion.fecha_registro)
            .all()
        )

    def obtener_por_momento(
        self, id_inscripcion: int, id_asignatura: int, momento: str
    ) -> list[Calificacion]:
        """Retorna las notas de un momento específico (ej: 'Momento 1')."""
        return (
            self.session.query(Calificacion)
            .filter(
                Calificacion.id_inscripcion == id_inscripcion,
                Calificacion.id_asignatura  == id_asignatura,
                Calificacion.momento        == momento,
            )
            .all()
        )

    def obtener_por_seccion_y_asignatura(
        self, id_seccion: int, id_asignatura: int
    ) -> list[Calificacion]:
        """
        Retorna todas las calificaciones de una asignatura
        para toda una sección. Útil para reportes por sección.
        """
        from database.models import Inscripcion
        return (
            self.session.query(Calificacion)
            .join(Inscripcion, Inscripcion.id_inscripcion == Calificacion.id_inscripcion)
            .filter(
                Inscripcion.id_seccion      == id_seccion,
                Calificacion.id_asignatura  == id_asignatura,
            )
            .order_by(Calificacion.momento)
            .all()
        )
