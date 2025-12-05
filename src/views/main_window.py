"""
Vista principal del sistema de gestión de tareas usando CustomTkinter.
Proporciona una interfaz gráfica moderna y funcional.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta


class MainWindow:
    """
    Ventana principal de la aplicación.
    Interfaz gráfica moderna con CustomTkinter.
    """

    def __init__(self, controller):
        """
        Inicializa la ventana principal.

        Args:
            controller (TaskController): Controlador de tareas
        """
        self.controller = controller

        # Configuración de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Gestión de Tareas - MaxHeap & AVL")
        self.root.geometry("1200x900")

        # Crear interfaz
        self._create_widgets()

        # Actualizar vista inicial
        self.refresh_task_list()
        self.update_statistics()
        self.update_visualizations()

    def _create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # ========== FRAME SUPERIOR: ESTADÍSTICAS ==========
        stats_header_frame = ctk.CTkFrame(self.root)
        stats_header_frame.pack(fill="x", padx=10, pady=10)

        stats_title = ctk.CTkLabel(
            stats_header_frame,
            text="Estadísticas de Tareas",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        stats_title.pack(pady=5)

        self.stats_label = ctk.CTkLabel(
            stats_header_frame,
            text="",
            font=ctk.CTkFont(size=13),
            justify="center"
        )
        self.stats_label.pack(pady=5)

        # ========== CONTENEDOR PRINCIPAL ==========
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
