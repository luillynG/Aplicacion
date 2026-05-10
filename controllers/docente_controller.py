from sqlalchemy.orm import Session
from database.models import Docente, Asignatura
from services.docente_service import DocenteService
from repositories.asignatura_repository import AsignaturaRepository


class DocenteController:
    """
    Orquesta el registro y consulta de docentes y asignaturas.
    """

    def __init__(self, session: Session):
        self.service         = DocenteService(session)
        self.repo_asignatura = AsignaturaRepository(session)

    # ── Docentes ───────────────────────────────────────────────────────────────
    def registrar_docente(
        self,
        cedula:       str,
        nombres:      str,
        apellidos:    str,
        especialidad: str = "",
        correo:       str = "",
        telefono:     str = "",
    ) -> tuple[bool, str]:
        exito, mensaje, _ = self.service.registrar_docente(
            cedula, nombres, apellidos, especialidad, correo, telefono
        )
        return exito, mensaje

    def asignar_materia(
        self, id_docente: int, id_asignatura: int
    ) -> tuple[bool, str]:
        return self.service.asignar_materia(id_docente, id_asignatura)

    def obtener_todos(self) -> list[Docente]:
        return self.service.obtener_todos()

    def obtener_por_id(self, id_docente: int) -> Docente | None:
        return self.service.obtener_por_id(id_docente)

    # ── Asignaturas ────────────────────────────────────────────────────────────
    def registrar_asignatura(self, nombre_materia: str) -> tuple[bool, str]:
        if not nombre_materia.strip():
            return False, "El nombre de la asignatura es obligatorio."

        asignatura = Asignatura(nombre_materia=nombre_materia.strip().title())
        try:
            self.repo_asignatura.agregar(asignatura)
            return True, "Asignatura registrada correctamente."
        except Exception as e:
            return False, f"Error al registrar asignatura: {e}"

    def obtener_asignaturas(self) -> list[Asignatura]:
        return self.repo_asignatura.obtener_todos()
