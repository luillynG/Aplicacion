from repositories.base_repository        import BaseRepository
from repositories.estudiante_repository  import EstudianteRepository
from repositories.docente_repository     import DocenteRepository
from repositories.asignatura_repository  import AsignaturaRepository
from repositories.año_seccion_repository import AñoSeccionRepository
from repositories.inscripcion_repository import InscripcionRepository
from repositories.asistencia_repository  import AsistenciaRepository
from repositories.calificacion_repository import CalificacionRepository

__all__ = [
    "BaseRepository",
    "EstudianteRepository",
    "DocenteRepository",
    "AsignaturaRepository",
    "AñoSeccionRepository",
    "InscripcionRepository",
    "AsistenciaRepository",
    "CalificacionRepository",
]
