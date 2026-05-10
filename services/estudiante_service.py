from datetime import date
from sqlalchemy.orm import Session
from database.models import Estudiante, Representante
from repositories.estudiante_repository   import EstudianteRepository
from repositories.inscripcion_repository  import InscripcionRepository
from repositories.año_seccion_repository  import AñoSeccionRepository


class EstudianteService:
    """
    Gestiona toda la lógica de negocio relacionada con
    estudiantes, representantes e inscripciones.
    """

    def __init__(self, session: Session):
        self.session     = session
        self.repo        = EstudianteRepository(session)
        self.repo_insc   = InscripcionRepository(session)
        self.repo_seccion = AñoSeccionRepository(session)

    # ── Registro ───────────────────────────────────────────────────────────────
    def registrar_estudiante(
        self,
        cedula:           str,
        nombres:          str,
        apellidos:        str,
        fecha_nacimiento: date,
        id_representante: int,
        direccion:        str = "",
    ) -> tuple[bool, str, Estudiante | None]:
        """
        Registra un nuevo estudiante.
        Retorna (éxito, mensaje, objeto_estudiante).
        """
        # Validar que la cédula no esté duplicada
        if self.repo.obtener_por_cedula(cedula):
            return False, f"Ya existe un estudiante con la cédula {cedula}.", None

        # Validar que los campos obligatorios no estén vacíos
        if not cedula.strip() or not nombres.strip() or not apellidos.strip():
            return False, "Cédula, nombres y apellidos son obligatorios.", None

        estudiante = Estudiante(
            cedula           = cedula.strip(),
            nombres          = nombres.strip().title(),
            apellidos        = apellidos.strip().title(),
            fecha_nacimiento = fecha_nacimiento,
            direccion        = direccion.strip(),
            id_representante = id_representante,
        )

        try:
            self.repo.agregar(estudiante)
            return True, "Estudiante registrado exitosamente.", estudiante
        except Exception as e:
            return False, f"Error al registrar estudiante: {e}", None

    # ── Inscripción ────────────────────────────────────────────────────────────
    def inscribir_estudiante(
        self,
        id_estudiante:  int,
        id_seccion:     int,
        periodo_escolar: str,
    ) -> tuple[bool, str]:
        """
        Inscribe un estudiante en una sección.
        Valida que no esté ya inscrito en el mismo período.
        """
        from database.models import Inscripcion

        # Verificar que el estudiante existe
        estudiante = self.repo.obtener_por_id(id_estudiante)
        if not estudiante:
            return False, "Estudiante no encontrado."

        # Verificar que no esté inscrito en este período
        ya_inscrito = self.repo_insc.obtener_por_estudiante_y_periodo(
            id_estudiante, periodo_escolar
        )
        if ya_inscrito:
            return False, f"El estudiante ya está inscrito en el período {periodo_escolar}."

        inscripcion = Inscripcion(
            id_estudiante = id_estudiante,
            id_seccion    = id_seccion,
        )

        try:
            self.repo_insc.agregar(inscripcion)
            return True, "Estudiante inscrito exitosamente."
        except Exception as e:
            return False, f"Error al inscribir estudiante: {e}"

    # ── Consultas ──────────────────────────────────────────────────────────────
    def obtener_todos(self) -> list[Estudiante]:
        return self.repo.obtener_todos()

    def buscar(self, texto: str) -> list[Estudiante]:
        return self.repo.buscar_por_nombre(texto)

    def obtener_por_seccion(self, id_seccion: int) -> list[Estudiante]:
        return self.repo.obtener_por_seccion(id_seccion)

    def obtener_por_id(self, id_estudiante: int) -> Estudiante | None:
        return self.repo.obtener_por_id(id_estudiante)

    # ── Actualizar ─────────────────────────────────────────────────────────────
    def actualizar_estudiante(
        self,
        id_estudiante:    int,
        nombres:          str,
        apellidos:        str,
        fecha_nacimiento: date,
        direccion:        str,
    ) -> tuple[bool, str]:
        estudiante = self.repo.obtener_por_id(id_estudiante)
        if not estudiante:
            return False, "Estudiante no encontrado."

        estudiante.nombres          = nombres.strip().title()
        estudiante.apellidos        = apellidos.strip().title()
        estudiante.fecha_nacimiento = fecha_nacimiento
        estudiante.direccion        = direccion.strip()

        try:
            self.repo.actualizar()
            return True, "Datos actualizados correctamente."
        except Exception as e:
            return False, f"Error al actualizar: {e}"
