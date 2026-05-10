from datetime import date
from sqlalchemy.orm import Session
from database.models import Calificacion
from repositories.calificacion_repository import CalificacionRepository
from repositories.inscripcion_repository  import InscripcionRepository


# Momentos válidos según el sistema educativo venezolano
MOMENTOS_VALIDOS  = ("Momento 1", "Momento 2", "Momento 3")
TIPOS_NOTA_VALIDOS = ("Evaluacion", "Trabajo", "Examen")


class CalificacionService:
    """
    Gestiona el registro y consulta de calificaciones,
    incluyendo el cálculo de promedios por momento y definitiva.
    """

    def __init__(self, session: Session):
        self.repo      = CalificacionRepository(session)
        self.repo_insc = InscripcionRepository(session)

    # ── Registro ───────────────────────────────────────────────────────────────
    def registrar_nota(
        self,
        id_inscripcion: int,
        id_asignatura:  int,
        momento:        str,
        puntaje:        float,
        tipo_de_nota:   str,
        fecha_registro: date | None = None,
    ) -> tuple[bool, str]:
        """
        Registra una calificación con validaciones de rango y campos válidos.
        """
        # Validar momento
        if momento not in MOMENTOS_VALIDOS:
            return False, f"Momento inválido. Use: {', '.join(MOMENTOS_VALIDOS)}"

        # Validar tipo de nota
        if tipo_de_nota not in TIPOS_NOTA_VALIDOS:
            return False, f"Tipo de nota inválido. Use: {', '.join(TIPOS_NOTA_VALIDOS)}"

        # Validar rango de puntaje (sistema venezolano: 1 al 20)
        if not (1 <= puntaje <= 20):
            return False, "El puntaje debe estar entre 1 y 20."

        nota = Calificacion(
            id_inscripcion = id_inscripcion,
            id_asignatura  = id_asignatura,
            momento        = momento,
            puntaje        = round(puntaje, 2),
            fecha_registro = fecha_registro or date.today(),
            tipo_de_nota   = tipo_de_nota,
        )

        try:
            self.repo.agregar(nota)
            return True, "Calificación registrada exitosamente."
        except Exception as e:
            return False, f"Error al registrar calificación: {e}"

    # ── Cálculos ───────────────────────────────────────────────────────────────
    def calcular_promedio_momento(
        self,
        id_inscripcion: int,
        id_asignatura:  int,
        momento:        str,
    ) -> float | None:
        """
        Calcula el promedio de todas las notas de un momento específico.
        Retorna None si no hay notas registradas.
        """
        notas = self.repo.obtener_por_momento(id_inscripcion, id_asignatura, momento)
        if not notas:
            return None
        return round(sum(n.puntaje for n in notas) / len(notas), 2)

    def calcular_definitiva(
        self,
        id_inscripcion: int,
        id_asignatura:  int,
    ) -> dict:
        """
        Calcula la nota definitiva como promedio de los 3 momentos.
        Retorna un dict con los promedios por momento y la definitiva.

        Ejemplo de retorno:
        {
            "Momento 1": 14.5,
            "Momento 2": 16.0,
            "Momento 3": None,   # aún no tiene notas
            "definitiva": None   # solo se calcula si los 3 momentos tienen notas
        }
        """
        resultado = {}
        promedios = []

        for momento in MOMENTOS_VALIDOS:
            prom = self.calcular_promedio_momento(id_inscripcion, id_asignatura, momento)
            resultado[momento] = prom
            if prom is not None:
                promedios.append(prom)

        # La definitiva solo se calcula cuando los 3 momentos tienen notas
        if len(promedios) == 3:
            resultado["definitiva"] = round(sum(promedios) / 3, 2)
        else:
            resultado["definitiva"] = None

        return resultado

    # ── Consultas ──────────────────────────────────────────────────────────────
    def obtener_notas_estudiante(
        self,
        id_inscripcion: int,
        id_asignatura:  int,
    ) -> list[Calificacion]:
        return self.repo.obtener_por_inscripcion_y_asignatura(
            id_inscripcion, id_asignatura
        )

    def obtener_notas_seccion(
        self,
        id_seccion:    int,
        id_asignatura: int,
    ) -> list[Calificacion]:
        """Útil para generar reportes de rendimiento por sección."""
        return self.repo.obtener_por_seccion_y_asignatura(id_seccion, id_asignatura)
