from datetime import date
from sqlalchemy.orm import Session
from database.models import Calificacion
from services.calificacion_service import CalificacionService


class CalificacionesController:
    """
    Orquesta el registro y consulta de calificaciones.
    """

    def __init__(self, session: Session):
        self.service = CalificacionService(session)

    def registrar_nota(
        self,
        id_inscripcion: int,
        id_asignatura:  int,
        momento:        str,
        puntaje:        float,
        tipo_de_nota:   str,
        fecha_registro: date | None = None,
    ) -> tuple[bool, str]:
        return self.service.registrar_nota(
            id_inscripcion, id_asignatura,
            momento, puntaje, tipo_de_nota, fecha_registro
        )

    def obtener_notas(
        self,
        id_inscripcion: int,
        id_asignatura:  int,
    ) -> list[Calificacion]:
        return self.service.obtener_notas_estudiante(id_inscripcion, id_asignatura)

    def obtener_definitiva(
        self,
        id_inscripcion: int,
        id_asignatura:  int,
    ) -> dict:
        """
        Retorna el resumen completo de calificaciones:
        promedios por momento y nota definitiva.
        """
        return self.service.calcular_definitiva(id_inscripcion, id_asignatura)

    def obtener_notas_seccion(
        self,
        id_seccion:    int,
        id_asignatura: int,
    ) -> list[Calificacion]:
        """Para la generación de reportes por sección."""
        return self.service.obtener_notas_seccion(id_seccion, id_asignatura)
