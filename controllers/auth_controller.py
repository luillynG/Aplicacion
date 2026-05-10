import config


class AuthController:
    """
    Controla el acceso al sistema.
    Usa las credenciales definidas en config.py.
    """

    def __init__(self):
        self._sesion_activa = False

    def iniciar_sesion(self, usuario: str, contrasena: str) -> tuple[bool, str]:
        """
        Verifica las credenciales del administrador.
        Retorna (éxito, mensaje).
        """
        if not usuario.strip() or not contrasena.strip():
            return False, "Usuario y contraseña son obligatorios."

        if config.verificar_credenciales(usuario.strip(), contrasena):
            self._sesion_activa = True
            return True, "Acceso concedido."

        return False, "Usuario o contraseña incorrectos."

    def cerrar_sesion(self) -> None:
        self._sesion_activa = False

    @property
    def hay_sesion_activa(self) -> bool:
        return self._sesion_activa
