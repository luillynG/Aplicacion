import customtkinter as ctk
from sqlalchemy.orm import Session
from assets.theme import *
from repositories.base_repository import BaseRepository
from database.models import Estudiante, Docente, Asignatura, AñoSeccion
import config


class InicioView(ctk.CTkFrame):
    """
    Panel de inicio con tarjetas de resumen del sistema.
    Primera vista que se muestra tras el login.
    """

    def __init__(self, parent, session: Session, **kwargs):
        super().__init__(parent, fg_color=FONDO_APP, corner_radius=0)
        self.session = session
        self._construir_ui()

    def _construir_ui(self):
        # ── Encabezado ─────────────────────────────────────────────────────────
        encabezado = ctk.CTkFrame(self, fg_color=FONDO_CARD, corner_radius=0)
        encabezado.pack(fill="x", padx=0, pady=(0, 0))

        ctk.CTkFrame(encabezado, height=4, fg_color=DORADO, corner_radius=0).pack(fill="x")

        contenido_enc = ctk.CTkFrame(encabezado, fg_color="transparent")
        contenido_enc.pack(fill="x", padx=PADDING_CARD, pady=20)

        ctk.CTkLabel(
            contenido_enc,
            text=f"Bienvenido al Sistema de Gestión Académica",
            font=FUENTE_TITULO,
            text_color=TEXTO_PRIMARIO,
        ).pack(anchor="w")

        ctk.CTkLabel(
            contenido_enc,
            text=config.APP_LICEO,
            font=FUENTE_NORMAL,
            text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", pady=(4, 0))

        # ── Tarjetas de resumen ────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="Resumen del sistema",
            font=FUENTE_SUBTITULO,
            text_color=TEXTO_PRIMARIO,
        ).pack(anchor="w", padx=PADDING_CARD, pady=(24, 12))

        fila_cards = ctk.CTkFrame(self, fg_color="transparent")
        fila_cards.pack(fill="x", padx=PADDING_CARD)

        tarjetas = [
            ("👨‍🎓", "Estudiantes",  self._contar(Estudiante), AZUL_OSCURO),
            ("👨‍🏫", "Docentes",     self._contar(Docente),    AZUL_CLARO),
            ("📚", "Asignaturas",  self._contar(Asignatura),  DORADO),
            ("🏫", "Secciones",    self._contar(AñoSeccion),  ROJO_ACENTO),
        ]

        for icono, titulo, valor, color in tarjetas:
            self._crear_card(fila_cards, icono, titulo, valor, color)

        # ── Accesos rápidos ────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="Accesos rápidos",
            font=FUENTE_SUBTITULO,
            text_color=TEXTO_PRIMARIO,
        ).pack(anchor="w", padx=PADDING_CARD, pady=(32, 12))

        fila_accesos = ctk.CTkFrame(self, fg_color="transparent")
        fila_accesos.pack(fill="x", padx=PADDING_CARD)

        accesos = [
            ("➕  Nueva matrícula",    AZUL_OSCURO, AZUL_CLARO),
            ("📝  Registrar notas",    AZUL_CLARO,  AZUL_OSCURO),
            ("📋  Pasar asistencia",   DORADO,      "#A07800"),
            ("📊  Generar reporte",    ROJO_ACENTO, "#7A1E2E"),
        ]

        for texto, color, hover in accesos:
            ctk.CTkButton(
                fila_accesos,
                text=texto,
                height=44,
                font=FUENTE_BOTON,
                fg_color=color,
                hover_color=hover,
                text_color="white",
                corner_radius=RADIO_BOTON,
            ).pack(side="left", padx=(0, 12))

    def _crear_card(self, parent, icono, titulo, valor, color):
        card = ctk.CTkFrame(
            parent,
            fg_color=FONDO_CARD,
            corner_radius=12,
            border_width=1,
            border_color=BORDE_SUAVE,
        )
        card.pack(side="left", expand=True, fill="x", padx=(0, 12))

        # Barra de color superior
        ctk.CTkFrame(card, height=4, fg_color=color, corner_radius=0).pack(
            fill="x"
        )

        contenido = ctk.CTkFrame(card, fg_color="transparent")
        contenido.pack(fill="x", padx=18, pady=16)

        ctk.CTkLabel(
            contenido,
            text=icono,
            font=("Segoe UI Emoji", 26),
            text_color=color,
            fg_color="transparent",
        ).pack(anchor="w")

        ctk.CTkLabel(
            contenido,
            text=str(valor),
            font=("Georgia", 28, "bold"),
            text_color=TEXTO_PRIMARIO,
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkLabel(
            contenido,
            text=titulo,
            font=FUENTE_PEQUEÑA,
            text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

    def _contar(self, modelo) -> int:
        """Cuenta los registros de un modelo en la BD."""
        try:
            repo = BaseRepository(self.session, modelo)
            return len(repo.obtener_todos())
        except Exception:
            return 0
