from typing import Optional
from sqlalchemy.orm import Session
from database.models import Estudiante
from repositories.base_repository import BaseRepository


class EstudianteRepository(BaseRepository[Estudiante]):

    def __init__(self, session: Session):
        super().__init__(session, Estudiante)

    def obtener_por_cedula(self, cedula: str) -> Optional[Estudiante]:
        """Busca un estudiante por su cédula."""
        return (
            self.session.query(Estudiante)
            .filter(Estudiante.cedula == cedula)
            .first()
        )

    def buscar_por_nombre(self, texto: str) -> list[Estudiante]:
        """Busca estudiantes cuyo nombre o apellido contenga el texto."""
        patron = f"%{texto}%"
        return (
            self.session.query(Estudiante)
            .filter(
                Estudiante.nombres.ilike(patron) |
                Estudiante.apellidos.ilike(patron)
            )
            .order_by(Estudiante.apellidos)
            .all()
        )

    def obtener_por_seccion(self, id_seccion: int) -> list[Estudiante]:
        """Retorna todos los estudiantes inscritos en una sección."""
        from database.models import Inscripcion
        return (
            self.session.query(Estudiante)
            .join(Inscripcion, Inscripcion.id_estudiante == Estudiante.id_estudiante)
            .filter(Inscripcion.id_seccion == id_seccion)
            .order_by(Estudiante.apellidos)
            .all()
        )
