from datetime import date
from sqlalchemy.orm import Session
from database.models import Asistencia
from repositories.asistencia_repository  import AsistenciaRepository
from repositories.inscripcion_repository import InscripcionRepository


ESTADOS_VALIDOS = ("Presente", "Ausente", "Justificado")


class AsistenciaService:
    """
    Gestiona el registro y consulta de asistencia,
    con validaciones para evitar duplicados por día.
    """

    def __init__(self, session: Session):
        self.repo      = AsistenciaRepository(session)
        self.repo_insc = InscripcionRepository(session)

    # ── Registro individual ────────────────────────────────────────────────────
    def registrar_asistencia(
        self,
        id_inscripcion: int,
        fecha:          date,
        estado:         str,
    ) -> tuple[bool, str]:
        """
        Registra la asistencia de un estudiante en una fecha.
        Valida que no exista un registro previo para ese día.
        """
        if estado not in ESTADOS_VALIDOS:
            return False, f"Estado inválido. Use: {', '.join(ESTADOS_VALIDOS)}"

        if self.repo.ya_registrada(id_inscripcion, fecha):
            return False, f"Ya existe un registro de asistencia para esta fecha."

        asistencia = Asistencia(
            id_inscripcion = id_inscripcion,
            fecha          = fecha,
            estado         = estado,
        )

        try:
            self.repo.agregar(asistencia)
            return True, "Asistencia registrada correctamente."
        except Exception as e:
            return False, f"Error al registrar asistencia: {e}"

    # ── Registro masivo por sección ────────────────────────────────────────────
    def registrar_asistencia_seccion(
        self,
        id_seccion: int,
        fecha:      date,
        registros:  dict[int, str],  # {id_inscripcion: estado}
    ) -> tuple[int, int, list[str]]:
        """
        Registra la asistencia de toda una sección en un solo paso.
        Retorna (exitosos, fallidos, lista_de_errores).
        """
        exitosos = 0
        fallidos = 0
        errores  = []

        for id_inscripcion, estado in registros.items():
            exito, mensaje = self.registrar_asistencia(id_inscripcion, fecha, estado)
            if exito:
                exitosos += 1
            else:
                fallidos += 1
                errores.append(f"Inscripción {id_inscripcion}: {mensaje}")

        return exitosos, fallidos, errores

    # ── Consultas ──────────────────────────────────────────────────────────────
    def obtener_historial(self, id_inscripcion: int) -> list[Asistencia]:
        return self.repo.obtener_por_inscripcion(id_inscripcion)

    def obtener_asistencia_del_dia(
        self, fecha: date, id_seccion: int
    ) -> list[Asistencia]:
        return self.repo.obtener_por_fecha_y_seccion(fecha, id_seccion)

    def calcular_resumen(self, id_inscripcion: int) -> dict:
        """
        Calcula el resumen de asistencia de un estudiante.

        Retorna:
        {
            "total":       30,
            "presentes":   25,
            "ausentes":     3,
            "justificados": 2,
            "porcentaje":  83.33
        }
        """
        historial = self.repo.obtener_por_inscripcion(id_inscripcion)

        total        = len(historial)
        presentes    = sum(1 for a in historial if a.estado == "Presente")
        ausentes     = sum(1 for a in historial if a.estado == "Ausente")
        justificados = sum(1 for a in historial if a.estado == "Justificado")
        porcentaje   = round((presentes / total * 100), 2) if total > 0 else 0.0

        return {
            "total":        total,
            "presentes":    presentes,
            "ausentes":     ausentes,
            "justificados": justificados,
            "porcentaje":   porcentaje,
        }
