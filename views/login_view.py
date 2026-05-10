import customtkinter as ctk
from assets.theme import *
from controllers.auth_controller import AuthController


class LoginView(ctk.CTkToplevel):
    """
    Ventana de autenticación. Se muestra antes de la ventana principal.
    Bloquea el acceso hasta que las credenciales sean correctas.
    """

    def __init__(self, parent, auth_controller: AuthController, on_success):
        super().__init__(parent)

        self.auth        = auth_controller
        self.on_success  = on_success  # Callback al autenticar correctamente

        # ── Configuración de ventana ───────────────────────────────────────────
        self.title("Acceso al Sistema")
        self.geometry("420x520")
        self.resizable(False, False)
        self.configure(fg_color=FONDO_APP)
        self.grab_set()   # Modal: bloquea la ventana padre
        self.focus_set()

        # Centrar en pantalla
        self.after(10, self._centrar)
        self._construir_ui()

    def _centrar(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  // 2) - (420 // 2)
        y = (self.winfo_screenheight() // 2) - (520 // 2)
        self.geometry(f"420x520+{x}+{y}")

    def _construir_ui(self):
        # ── Encabezado institucional ───────────────────────────────────────────
        encabezado = ctk.CTkFrame(self, fg_color=AZUL_OSCURO, corner_radius=0)
        encabezado.pack(fill="x")

        ctk.CTkLabel(
            encabezado,
            text="🏫",
            font=("Segoe UI Emoji", 40),
            fg_color="transparent",
            text_color=DORADO,
        ).pack(pady=(28, 4))

        ctk.CTkLabel(
            encabezado,
            text="Liceo Nacional",
            font=("Georgia", 11),
            text_color=TEXTO_SIDEBAR,
            fg_color="transparent",
        ).pack()

        ctk.CTkLabel(
            encabezado,
            text='"Antonio José de Sucre"',
            font=("Georgia", 14, "bold"),
            text_color=DORADO,
            fg_color="transparent",
        ).pack(pady=(0, 24))

        # ── Formulario ─────────────────────────────────────────────────────────
        form = ctk.CTkFrame(self, fg_color=FONDO_APP, corner_radius=0)
        form.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(
            form,
            text="Iniciar Sesión",
            font=FUENTE_SUBTITULO,
            text_color=TEXTO_PRIMARIO,
        ).pack(anchor="w", pady=(0, 20))

        # Campo usuario
        ctk.CTkLabel(
            form, text="Usuario",
            font=FUENTE_PEQUEÑA,
            text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        self.entrada_usuario = ctk.CTkEntry(
            form,
            placeholder_text="Ingrese su usuario",
            height=ALTO_ENTRADA,
            font=FUENTE_NORMAL,
            fg_color=FONDO_CARD,
            border_color=BORDE_SUAVE,
            text_color=TEXTO_PRIMARIO,
            corner_radius=RADIO_BOTON,
        )
        self.entrada_usuario.pack(fill="x", pady=(4, 14))

        # Campo contraseña
        ctk.CTkLabel(
            form, text="Contraseña",
            font=FUENTE_PEQUEÑA,
            text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        self.entrada_contrasena = ctk.CTkEntry(
            form,
            placeholder_text="Ingrese su contraseña",
            show="●",
            height=ALTO_ENTRADA,
            font=FUENTE_NORMAL,
            fg_color=FONDO_CARD,
            border_color=BORDE_SUAVE,
            text_color=TEXTO_PRIMARIO,
            corner_radius=RADIO_BOTON,
        )
        self.entrada_contrasena.pack(fill="x", pady=(4, 6))

        # Mensaje de error (oculto inicialmente)
        self.lbl_error = ctk.CTkLabel(
            form, text="",
            font=FUENTE_PEQUEÑA,
            text_color=ERROR,
        )
        self.lbl_error.pack(anchor="w", pady=(0, 16))

        # Botón ingresar
        self.btn_ingresar = ctk.CTkButton(
            form,
            text="Ingresar",
            height=ALTO_BOTON,
            font=FUENTE_BOTON,
            fg_color=AZUL_OSCURO,
            hover_color=AZUL_CLARO,
            text_color="white",
            corner_radius=RADIO_BOTON,
            command=self._intentar_login,
        )
        self.btn_ingresar.pack(fill="x")

        # ── Pie ────────────────────────────────────────────────────────────────
        ctk.CTkLabel(
            form,
            text="Sistema de Gestión Académica v1.0",
            font=FUENTE_PEQUEÑA,
            text_color=TEXTO_SECUNDARIO,
        ).pack(side="bottom", pady=(0, 4))

        # Enter activa el login
        self.entrada_contrasena.bind("<Return>", lambda e: self._intentar_login())
        self.entrada_usuario.bind("<Return>",    lambda e: self.entrada_contrasena.focus())

        # Foco inicial
        self.after(100, self.entrada_usuario.focus)

    def _intentar_login(self):
        usuario    = self.entrada_usuario.get()
        contrasena = self.entrada_contrasena.get()

        exito, mensaje = self.auth.iniciar_sesion(usuario, contrasena)

        if exito:
            self.lbl_error.configure(text="")
            self.destroy()
            self.on_success()
        else:
            self.lbl_error.configure(text=f"⚠  {mensaje}")
            self.entrada_contrasena.delete(0, "end")
            self.entrada_contrasena.focus()
