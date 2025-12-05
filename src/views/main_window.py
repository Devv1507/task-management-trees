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

        # ========== PANEL DERECHO: LISTA DE TAREAS ==========
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=0)

        # Título y controles
        control_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        control_frame.pack(fill="x", padx=15, pady=15)

        tasks_title = ctk.CTkLabel(
            control_frame,
            text="Lista de Tareas",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        tasks_title.pack(side="left")

        # Botones de acción
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(side="right")

        complete_btn = ctk.CTkButton(
            button_frame,
            text="✓ Completar Prioritaria",
            command=self.complete_highest_priority,
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=160
        )
        complete_btn.pack(side="left", padx=5)

        refresh_btn = ctk.CTkButton(
            button_frame,
            text="Actualizar",
            command=self.refresh_task_list,
            width=100
        )
        refresh_btn.pack(side="left", padx=5)

        # Frame de búsqueda
        search_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(0, 10))

        search_label = ctk.CTkLabel(search_frame, text="Buscar por ID:")
        search_label.pack(side="left", padx=(0, 10))

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="ID de tarea", width=100)
        self.search_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_task,
            width=80
        )
        search_btn.pack(side="left", padx=5)

        delete_btn = ctk.CTkButton(
            search_frame,
            text="Eliminar por ID",
            command=self.delete_task_by_id,
            fg_color="#F44336",
            hover_color="#D32F2F",
            width=120
        )
        delete_btn.pack(side="left", padx=5)

        # Lista de tareas
        self.tasks_textbox = ctk.CTkTextbox(
            right_panel,
            font=ctk.CTkFont(family="Courier New", size=12),
            wrap="none"
        )
        self.tasks_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))