from datetime import date
from sqlalchemy.orm import Session
from database.models import Estudiante, Representante
from services.estudiante_service import EstudianteService
from repositories.base_repository import BaseRepository


class EstudianteController:
    """
    Orquesta las operaciones de matrícula estudiantil.
    Recibe datos crudos desde la UI y delega al servicio.
    """

    def __init__(self, session: Session):
        self.session = session
        self.service = EstudianteService(session)
        # Repositorio directo para representantes (operaciones simples)
        self._repo_rep = BaseRepository(session, Representante)

    # ── Estudiantes ────────────────────────────────────────────────────────────
    def registrar(
        self,
        cedula:           str,
        nombres:          str,
        apellidos:        str,
        fecha_nacimiento: date,
        id_representante: int,
        direccion:        str = "",
    ) -> tuple[bool, str]:
        exito, mensaje, _ = self.service.registrar_estudiante(
            cedula, nombres, apellidos,
            fecha_nacimiento, id_representante, direccion
        )
        return exito, mensaje

    def actualizar(
        self,
        id_estudiante:    int,
        nombres:          str,
        apellidos:        str,
        fecha_nacimiento: date,
        direccion:        str,
    ) -> tuple[bool, str]:
        return self.service.actualizar_estudiante(
            id_estudiante, nombres, apellidos, fecha_nacimiento, direccion
        )

    def inscribir(
        self,
        id_estudiante:   int,
        id_seccion:      int,
        periodo_escolar: str,
    ) -> tuple[bool, str]:
        return self.service.inscribir_estudiante(
            id_estudiante, id_seccion, periodo_escolar
        )

    def obtener_todos(self) -> list[Estudiante]:
        return self.service.obtener_todos()

    def buscar(self, texto: str) -> list[Estudiante]:
        return self.service.buscar(texto)

    def obtener_por_id(self, id_estudiante: int) -> Estudiante | None:
        return self.service.obtener_por_id(id_estudiante)

    def obtener_por_seccion(self, id_seccion: int) -> list[Estudiante]:
        return self.service.obtener_por_seccion(id_seccion)

    # ── Representantes ─────────────────────────────────────────────────────────
    def registrar_representante(
        self,
        cedula:           str,
        nombres:          str,
        apellidos:        str,
        fecha_nacimiento: date,
        direccion:        str = "",
        telefono:         str = "",
        correo:           str = "",
    ) -> tuple[bool, str, int | None]:
        """
        Registra un representante y retorna su ID para vincularlo al estudiante.
        Retorna (éxito, mensaje, id_representante).
        """
        if not cedula.strip() or not nombres.strip() or not apellidos.strip():
            return False, "Cédula, nombres y apellidos son obligatorios.", None

        representante = Representante(
            cedula           = cedula.strip(),
            nombres          = nombres.strip().title(),
            apellidos        = apellidos.strip().title(),
            fecha_nacimiento = fecha_nacimiento,
            direccion        = direccion.strip(),
            telefono         = telefono.strip(),
            correo           = correo.strip(),
        )

        try:
            self._repo_rep.agregar(representante)
            return True, "Representante registrado.", representante.id_representante
        except Exception as e:
            return False, f"Error al registrar representante: {e}", None

    def obtener_representantes(self) -> list[Representante]:
        return self._repo_rep.obtener_todos()
