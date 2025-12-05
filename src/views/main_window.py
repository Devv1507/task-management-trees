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

        # ========== PANEL IZQUIERDO: AGREGAR TAREA ==========
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", padx=(0, 5), pady=0, expand=False)
        left_panel.configure(width=350)

        # Título del panel
        add_title = ctk.CTkLabel(
            left_panel,
            text="Agregar Nueva Tarea",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        add_title.pack(pady=(15, 10))

        # Descripción
        desc_label = ctk.CTkLabel(left_panel, text="Descripción:", anchor="w")
        desc_label.pack(pady=(10, 5), padx=20, fill="x")

        self.desc_entry = ctk.CTkTextbox(left_panel, height=100)
        self.desc_entry.pack(pady=(0, 10), padx=20, fill="x")

        # Prioridad
        priority_label = ctk.CTkLabel(left_panel, text="Prioridad:", anchor="w")
        priority_label.pack(pady=(10, 5), padx=20, fill="x")

        self.priority_var = ctk.StringVar(value="MEDIA")
        priority_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        priority_frame.pack(pady=(0, 10), padx=20, fill="x")

        priorities = [("ALTA", "#F44336"), ("MEDIA", "#FF9800"), ("BAJA", "#4CAF50")]
        for priority, color in priorities:
            radio = ctk.CTkRadioButton(
                priority_frame,
                text=priority,
                variable=self.priority_var,
                value=priority,
                fg_color=color,
                hover_color=color
            )
            radio.pack(side="left", padx=5)

        # Fecha de vencimiento
        date_label = ctk.CTkLabel(left_panel, text="Fecha de Vencimiento:", anchor="w")
        date_label.pack(pady=(10, 5), padx=20, fill="x")

        self.date_entry = ctk.CTkEntry(left_panel, placeholder_text="YYYY-MM-DD")
        self.date_entry.pack(pady=(0, 5), padx=20, fill="x")

        # Sugerencias de fecha
        date_buttons_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        date_buttons_frame.pack(pady=(0, 10), padx=20, fill="x")

        date_shortcuts = [("Hoy", 0), ("Mañana", 1), ("+7 días", 7)]
        for text, days in date_shortcuts:
            btn = ctk.CTkButton(
                date_buttons_frame,
                text=text,
                width=70,
                height=25,
                command=lambda d=days: self._set_date(d)
            )
            btn.pack(side="left", padx=2)

        # Botón agregar
        add_button = ctk.CTkButton(
            left_panel,
            text="Añadir Tarea",
            command=self.add_task,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1976D2",
            hover_color="#1565C0"
        )
        add_button.pack(pady=20, padx=20, fill="x")
