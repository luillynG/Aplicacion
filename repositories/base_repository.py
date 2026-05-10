from typing import TypeVar, Generic, Type, Optional
from sqlalchemy.orm import Session
from database.models import Base

# T representa cualquier modelo ORM (Estudiante, Docente, etc.)
T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Repositorio genérico con operaciones CRUD reutilizables.
    Todos los repositorios específicos heredan de esta clase.
    """

    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model   = model

    # ── CREATE ─────────────────────────────────────────────────────────────────
    def agregar(self, entidad: T) -> T:
        """Inserta un nuevo registro en la base de datos."""
        try:
            self.session.add(entidad)
            self.session.commit()
            self.session.refresh(entidad)
            return entidad
        except Exception as e:
            self.session.rollback()
            raise e

    # ── READ ───────────────────────────────────────────────────────────────────
    def obtener_por_id(self, id: int) -> Optional[T]:
        """Retorna un registro por su clave primaria, o None si no existe."""
        return self.session.get(self.model, id)

    def obtener_todos(self) -> list[T]:
        """Retorna todos los registros de la tabla."""
        return self.session.query(self.model).all()

    # ── UPDATE ─────────────────────────────────────────────────────────────────
    def actualizar(self) -> None:
        """
        Confirma los cambios realizados sobre una entidad ya cargada.
        Uso: modificar atributos del objeto y luego llamar actualizar().
        """
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    # ── DELETE ─────────────────────────────────────────────────────────────────
    def eliminar(self, entidad: T) -> None:
        """Elimina un registro de la base de datos."""
        try:
            self.session.delete(entidad)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
