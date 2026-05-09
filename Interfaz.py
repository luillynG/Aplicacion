import tkinter as tk
from tkinter import messagebox

class AppGestion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Académica - Liceo Antonio José de Sucre")
        self.root.geometry("500x400")

        tk.Label(root, text="Panel de Control Académico", font=("Arial", 16, "bold")).pack(pady=20)

        # Botones Principales (Solicitados por el profesor)
        btn_estilo = {"width": 30, "height": 2, "font": ("Arial", 10)}

        tk.Button(root, text="Registro de Matrícula", command=self.menu_matricula, **btn_estilo).pack(pady=10)
        tk.Button(root, text="Carga de Calificaciones", command=self.menu_notas, **btn_estilo).pack(pady=10)
        tk.Button(root, text="Control de Asistencia", command=self.menu_asistencia, **btn_estilo).pack(pady=10)
        tk.Button(root, text="Generar Reportes (Boletines)", command=self.generar_reportes, **btn_estilo).pack(pady=10)

    def menu_matricula(self):
        # Ventana hija para registrar un nuevo estudiante
        ventana_registro = tk.Toplevel(self.root)
        ventana_registro.title("Registro de Nuevo Estudiante")
        ventana_registro.geometry("350x300")

        tk.Label(ventana_registro, text="Cédula:").pack(pady=5)
        entry_cedula = tk.Entry(ventana_registro)
        entry_cedula.pack()

        tk.Label(ventana_registro, text="Nombres:").pack(pady=5)
        entry_nombres = tk.Entry(ventana_registro)
        entry_nombres.pack()

        tk.Label(ventana_registro, text="Apellidos:").pack(pady=5)
        entry_apellidos = tk.Entry(ventana_registro)
        entry_apellidos.pack()

        tk.Label(ventana_registro, text="Año Escolar:").pack(pady=5)
        entry_anio = tk.Entry(ventana_registro)
        entry_anio.pack()

    def menu_notas(self):
        messagebox.showinfo("Módulo", "Abriendo panel de calificaciones...")

    def menu_asistencia(self):
        # Módulo planificado para mayo/junio según tu cronograma
        messagebox.showinfo("Módulo", "Accediendo al control de asistencia...")

    def generar_reportes(self):
        messagebox.showinfo("Reportes", "Generando listados académicos...")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGestion(root)
    root.mainloop()
