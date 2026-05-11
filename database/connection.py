from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from database.models import Base
import config

# ── Engine ────────────────────────────────────────────────────────────────────
# mysql+pymysql://usuario:contraseña@host:puerto/nombre_bd
DATABASE_URL = (
    f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    f"?charset=utf8mb4"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,          # True para ver el SQL generado en consola (útil al depurar)
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    pool_recycle=3600,   # Recicla conexiones cada 1 hora
)

# ── Session Factory ────────────────────────────────────────────────────────────
SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# ── Funciones públicas ─────────────────────────────────────────────────────────
def get_session() -> Session:
    """Retorna una sesión activa. El llamador es responsable de cerrarla."""
    return SessionFactory()


def init_db() -> bool:
    """
    Crea todas las tablas en la BD si no existen.
    Retorna True si la conexión fue exitosa, False si hubo error.
    """
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except OperationalError as e:
        print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
        return False
