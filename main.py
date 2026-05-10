import sys
import customtkinter as ctk
from database.connection import init_db, get_session
from views.main_window import MainWindow


def main():
    # ── Inicializar base de datos ──────────────────────────────────────────────
    if not init_db():
        import tkinter.messagebox as mb
        mb.showerror(
            "Error de conexión",
            "No se pudo conectar a la base de datos MySQL.\n\n"
            "Verifique que:\n"
            "  • El servidor MySQL esté corriendo\n"
            "  • Las credenciales en config.py sean correctas\n"
            "  • La base de datos 'sistema_escolar' exista"
        )
        sys.exit(1)

    # ── Sesión de base de datos ────────────────────────────────────────────────
    session = get_session()

    # ── Iniciar aplicación ─────────────────────────────────────────────────────
    try:
        app = MainWindow(session)
        app.mainloop()
    finally:
        session.close()


if __name__ == "__main__":
    main()
