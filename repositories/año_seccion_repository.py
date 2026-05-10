from sqlalchemy.orm import Session
from database.models import AñoSeccion
from repositories.base_repository import BaseRepository


class AñoSeccionRepository(BaseRepository[AñoSeccion]):

    def __init__(self, session: Session):
        super().__init__(session, AñoSeccion)

    def obtener_por_periodo(self, periodo_escolar: str) -> list[AñoSeccion]:
        """Retorna todas las secciones de un período escolar."""
        return (
            self.session.query(AñoSeccion)
            .filter(AñoSeccion.periodo_escolar == periodo_escolar)
            .order_by(AñoSeccion.año, AñoSeccion.seccion)
            .all()
        )

    def obtener_por_año_y_seccion(
        self, año: int, seccion: str, periodo_escolar: str
    ):
        """Busca una sección específica. Útil para evitar duplicados."""
        return (
            self.session.query(AñoSeccion)
            .filter(
                AñoSeccion.año             == año,
                AñoSeccion.seccion         == seccion,
                AñoSeccion.periodo_escolar == periodo_escolar,
            )
            .first()
        )
