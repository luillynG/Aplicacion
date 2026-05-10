from datetime import date
from sqlalchemy.orm import Session
from database.models import Asistencia
from services.asistencia_service import AsistenciaService


class AsistenciaController:
    """
    Orquesta el registro y consulta de asistencia.
    """

    def __init__(self, session: Session):
        self.service = AsistenciaService(session)

    def registrar(
        self,
        id_inscripcion: int,
        fecha:          date,
        estado:         str,
    ) -> tuple[bool, str]:
        return self.service.registrar_asistencia(id_inscripcion, fecha, estado)

    def registrar_seccion_completa(
        self,
        id_seccion: int,
        fecha:      date,
        registros:  dict[int, str],
    ) -> tuple[int, int, list[str]]:
        """
        Registra la asistencia de toda una sección.
        Retorna (exitosos, fallidos, errores).
        """
        return self.service.registrar_asistencia_seccion(
            id_seccion, fecha, registros
        )

    def obtener_historial(self, id_inscripcion: int) -> list[Asistencia]:
        return self.service.obtener_historial(id_inscripcion)

    def obtener_asistencia_del_dia(
        self, fecha: date, id_seccion: int
    ) -> list[Asistencia]:
        return self.service.obtener_asistencia_del_dia(fecha, id_seccion)

    def obtener_resumen(self, id_inscripcion: int) -> dict:
        """
        Retorna el resumen de asistencia para mostrar en la UI:
        total, presentes, ausentes, justificados y porcentaje.
        """
        return self.service.calcular_resumen(id_inscripcion)
