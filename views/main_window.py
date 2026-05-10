import customtkinter as ctk
from sqlalchemy.orm import Session
from assets.theme import *
from controllers.auth_controller import AuthController
from views.login_view import LoginView


class MainWindow(ctk.CTk):
    """
    Ventana principal de la aplicación.
    Contiene el sidebar de navegación y el área de contenido intercambiable.
    """

    def __init__(self, session: Session):
        super().__init__()

        self.session         = session
        self.auth_controller = AuthController()
        self.frame_actual    = None

        # ── Configuración de ventana ───────────────────────────────────────────
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Sistema de Gestión Académica — Liceo Antonio José de Sucre")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(fg_color=FONDO_APP)

        # Centrar ventana
        self.after(10, self._centrar)

        # Construir layout base (sidebar + área de contenido)
        self._construir_layout()

        # Ocultar ventana principal hasta que el login sea exitoso
        self.withdraw()
        self.after(100, self._mostrar_login)

    def _centrar(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  // 2) - (1100 // 2)
        y = (self.winfo_screenheight() // 2) - (680  // 2)
        self.geometry(f"1100x680+{x}+{y}")

    # ── Layout principal ───────────────────────────────────────────────────────
    def _construir_layout(self):
        # Sidebar izquierdo
        self.sidebar = ctk.CTkFrame(
            self,
            width=SIDEBAR_ANCHO,
            fg_color=AZUL_OSCURO,
            corner_radius=0,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # Ancho fijo

        # Área de contenido derecha
        self.area_contenido = ctk.CTkFrame(
            self,
            fg_color=FONDO_APP,
            corner_radius=0,
        )
        self.area_contenido.pack(side="left", fill="both", expand=True)

        self._construir_sidebar()

    def _construir_sidebar(self):
        # ── Logo / Encabezado ──────────────────────────────────────────────────
        encabezado = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        encabezado.pack(fill="x", pady=(20, 10), padx=16)

        ctk.CTkLabel(
            encabezado,
            text="🏫",
            font=("Segoe UI Emoji", 28),
            text_color=DORADO,
            fg_color="transparent",
        ).pack()

        ctk.CTkLabel(
            encabezado,
            text="Lic. Antonio José\nde Sucre",
            font=FUENTE_SIDEBAR_TITULO,
            text_color=DORADO,
            fg_color="transparent",
            justify="center",
        ).pack(pady=(4, 0))

        ctk.CTkLabel(
            encabezado,
            text="Gestión Académica",
            font=("Segoe UI", 9),
            text_color=TEXTO_SIDEBAR,
            fg_color="transparent",
        ).pack()

        # Separador
        ctk.CTkFrame(
            self.sidebar, height=1,
            fg_color=AZUL_MEDIO,
        ).pack(fill="x", padx=16, pady=16)

        # ── Menú de navegación ─────────────────────────────────────────────────
        self.botones_nav = {}

        opciones = [
            ("inicio",          "🏠",  "Inicio",          self._mostrar_inicio),
            ("estudiantes",     "👨‍🎓", "Estudiantes",      self._mostrar_estudiantes),
            ("calificaciones",  "📝",  "Calificaciones",   self._mostrar_calificaciones),
            ("asistencia",      "📋",  "Asistencia",       self._mostrar_asistencia),
            ("docentes",        "👨‍🏫", "Docentes",         self._mostrar_docentes),
            ("reportes",        "📊",  "Reportes",         self._mostrar_reportes),
        ]

        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10)

        for clave, icono, texto, comando in opciones:
            btn = ctk.CTkButton(
                nav_frame,
                text=f"  {icono}  {texto}",
                anchor="w",
                height=42,
                font=FUENTE_SIDEBAR,
                fg_color="transparent",
                hover_color=AZUL_MEDIO,
                text_color=TEXTO_SIDEBAR,
                corner_radius=RADIO_BOTON,
                command=lambda c=clave, cmd=comando: self._navegar(c, cmd),
            )
            btn.pack(fill="x", pady=2)
            self.botones_nav[clave] = btn

        # ── Pie del sidebar ────────────────────────────────────────────────────
        pie = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        pie.pack(side="bottom", fill="x", padx=10, pady=16)

        ctk.CTkFrame(
            self.sidebar, height=1,
            fg_color=AZUL_MEDIO,
        ).pack(side="bottom", fill="x", padx=16, pady=(0, 4))

        ctk.CTkButton(
            pie,
            text="  🚪  Cerrar Sesión",
            anchor="w",
            height=38,
            font=FUENTE_SIDEBAR,
            fg_color="transparent",
            hover_color=ROJO_ACENTO,
            text_color=TEXTO_SIDEBAR,
            corner_radius=RADIO_BOTON,
            command=self._cerrar_sesion,
        ).pack(fill="x")

    # ── Navegación ─────────────────────────────────────────────────────────────
    def _navegar(self, clave: str, comando):
        """Resalta el botón activo y ejecuta el comando de navegación."""
        for k, btn in self.botones_nav.items():
            if k == clave:
                btn.configure(
                    fg_color=AZUL_CLARO,
                    text_color=TEXTO_SIDEBAR_ACTIVO,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXTO_SIDEBAR,
                )
        comando()

    def mostrar_frame(self, frame_clase, **kwargs):
        """
        Destruye el frame actual y carga uno nuevo en el área de contenido.
        Todos los frames reciben la sesión de BD y la ventana principal.
        """
        if self.frame_actual:
            self.frame_actual.destroy()

        self.frame_actual = frame_clase(
            self.area_contenido,
            session=self.session,
            **kwargs
        )
        self.frame_actual.pack(fill="both", expand=True)

    # ── Destinos de navegación ─────────────────────────────────────────────────
    def _mostrar_inicio(self):
        from views.inicio_view import InicioView
        self.mostrar_frame(InicioView)

    def _mostrar_estudiantes(self):
        from views.matricula.lista_estudiantes import ListaEstudiantesView
        self.mostrar_frame(ListaEstudiantesView)

    def _mostrar_calificaciones(self):
        from views.calificaciones.vista_notas import VistaNotasView
        self.mostrar_frame(VistaNotasView)

    def _mostrar_asistencia(self):
        from views.asistencia.registro_asistencia import RegistroAsistenciaView
        self.mostrar_frame(RegistroAsistenciaView)

    def _mostrar_docentes(self):
        from views.docentes.lista_docentes import ListaDocentesView
        self.mostrar_frame(ListaDocentesView)

    def _mostrar_reportes(self):
        from views.reportes.panel_reportes import PanelReportesView
        self.mostrar_frame(PanelReportesView)

    # ── Login / Sesión ─────────────────────────────────────────────────────────
    def _mostrar_login(self):
        LoginView(self, self.auth_controller, on_success=self._on_login_exitoso)

    def _on_login_exitoso(self):
        """Callback ejecutado cuando el login es correcto."""
        self.deiconify()           # Muestra la ventana principal
        self._navegar("inicio", self._mostrar_inicio)

    def _cerrar_sesion(self):
        """Cierra sesión y vuelve al login."""
        self.auth_controller.cerrar_sesion()
        # Ocultar ventana y limpiar contenido
        if self.frame_actual:
            self.frame_actual.destroy()
            self.frame_actual = None
        # Resetear botones del sidebar
        for btn in self.botones_nav.values():
            btn.configure(fg_color="transparent", text_color=TEXTO_SIDEBAR)
        self.withdraw()
        self.after(100, self._mostrar_login)
