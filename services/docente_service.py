from sqlalchemy.orm import Session
from database.models import Docente
from repositories.docente_repository     import DocenteRepository
from repositories.asignatura_repository  import AsignaturaRepository


class DocenteService:
    """Gestiona el registro y consulta de docentes y sus asignaturas."""

    def __init__(self, session: Session):
        self.repo           = DocenteRepository(session)
        self.repo_asignatura = AsignaturaRepository(session)

    def registrar_docente(
        self,
        cedula:      str,
        nombres:     str,
        apellidos:   str,
        especialidad: str = "",
        correo:      str = "",
        telefono:    str = "",
    ) -> tuple[bool, str, Docente | None]:

        if self.repo.obtener_por_cedula(cedula):
            return False, f"Ya existe un docente con la cédula {cedula}.", None

        if not cedula.strip() or not nombres.strip() or not apellidos.strip():
            return False, "Cédula, nombres y apellidos son obligatorios.", None

        docente = Docente(
            cedula       = cedula.strip(),
            nombres      = nombres.strip().title(),
            apellidos    = apellidos.strip().title(),
            especialidad = especialidad.strip(),
            correo       = correo.strip(),
            telefono     = telefono.strip(),
        )

        try:
            self.repo.agregar(docente)
            return True, "Docente registrado exitosamente.", docente
        except Exception as e:
            return False, f"Error al registrar docente: {e}", None

    def asignar_materia(
        self, id_docente: int, id_asignatura: int
    ) -> tuple[bool, str]:
        """Asigna una materia a un docente mediante la tabla pivote."""
        from database.models import AsignaturaDocente

        docente    = self.repo.obtener_por_id(id_docente)
        asignatura = self.repo_asignatura.obtener_por_id(id_asignatura)

        if not docente:
            return False, "Docente no encontrado."
        if not asignatura:
            return False, "Asignatura no encontrada."

        # Verificar que no esté ya asignada
        if asignatura in docente.asignaturas:
            return False, "El docente ya tiene asignada esa materia."

        try:
            docente.asignaturas.append(asignatura)
            self.repo.actualizar()
            return True, "Materia asignada correctamente."
        except Exception as e:
            return False, f"Error al asignar materia: {e}"

    def obtener_todos(self) -> list[Docente]:
        return self.repo.obtener_con_asignaturas()

    def obtener_por_id(self, id_docente: int) -> Docente | None:
        return self.repo.obtener_por_id(id_docente)
