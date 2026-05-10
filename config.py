import hashlib

# ── Base de datos ──────────────────────────────────────────────────────────────
DB_HOST     = "localhost"
DB_PORT     = 3306
DB_NAME     = "sistema_escolar"
DB_USER     = "root"         # Cambiar según su configuración MySQL
DB_PASSWORD = "admin"         # Cambiar según su configuración MySQL


# ── Autenticación del administrador ───────────────────────────────────────────
# Las credenciales se almacenan como hash SHA-256, nunca en texto plano
def _hash(valor: str) -> str:
    return hashlib.sha256(valor.encode()).hexdigest()

ADMIN_USER          = "admin"
ADMIN_PASSWORD_HASH = _hash("liceo2026")  # Cambiar la contraseña aquí


def verificar_credenciales(usuario: str, contrasena: str) -> bool:
    """Verifica si el usuario y contraseña ingresados son correctos."""
    return (
        usuario   == ADMIN_USER and
        _hash(contrasena) == ADMIN_PASSWORD_HASH
    )


# ── Configuración general de la app ───────────────────────────────────────────
APP_NOMBRE  = "Sistema de Gestión Académica"
APP_LICEO   = "Liceo Nacional \"Antonio José de Sucre\""
APP_VERSION = "1.0.0"