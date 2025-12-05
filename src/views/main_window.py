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
        # Variables para el divisor arrastrable
        self.dragging = False
        self.drag_start_y = 0
        self.main_container_height = 500
        self.viz_frame_height = 280

        # ========== FRAME SUPERIOR: ESTADÍSTICAS ==========
        stats_header_frame = ctk.CTkFrame(self.root)
        stats_header_frame.pack(fill="x", padx=10, pady=10)

        stats_title = ctk.CTkLabel(
            stats_header_frame,
            text="Estadisticas",
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
        self.main_container = ctk.CTkFrame(self.root, height=self.main_container_height)
        self.main_container.pack(fill="both", expand=False, padx=10, pady=10)
        self.main_container.pack_propagate(False)

        # ========== PANEL IZQUIERDO: AGREGAR TAREA ==========
        left_panel = ctk.CTkScrollableFrame(self.main_container, width=330)
        left_panel.pack(side="left", fill="both", padx=(0, 5), pady=0, expand=False)

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
            text="Agregar Tarea",
            command=self.add_task,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1976D2",
            hover_color="#1565C0"
        )
        add_button.pack(pady=20, padx=20, fill="x")

        # ========== PANEL DERECHO: LISTA DE TAREAS ==========
        right_panel = ctk.CTkFrame(self.main_container)
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
            text="Completar Prioritaria",
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

        # ========== DIVISOR ARRASTRABLE ==========
        self.divider_frame = ctk.CTkFrame(self.root, height=8, cursor="sb_v_double_arrow")
        self.divider_frame.pack(fill="x", padx=10, pady=0)

        # Label del divisor
        divider_label = ctk.CTkLabel(
            self.divider_frame,
            text="═══ Arrastrar para redimensionar ═══",
            font=ctk.CTkFont(size=9),
            text_color="#888888"
        )
        divider_label.pack(pady=0)

        # Eventos de arrastre
        self.divider_frame.bind("<Button-1>", self._start_drag)
        self.divider_frame.bind("<B1-Motion>", self._on_drag)
        self.divider_frame.bind("<ButtonRelease-1>", self._stop_drag)
        divider_label.bind("<Button-1>", self._start_drag)
        divider_label.bind("<B1-Motion>", self._on_drag)
        divider_label.bind("<ButtonRelease-1>", self._stop_drag)

        # ========== PANEL INFERIOR: VISUALIZACIONES ==========
        self.viz_frame = ctk.CTkFrame(self.root, height=self.viz_frame_height)
        self.viz_frame.pack(fill="both", expand=False, padx=10, pady=(0, 10))
        self.viz_frame.pack_propagate(False)

        viz_title = ctk.CTkLabel(
            self.viz_frame,
            text="Visualizacion de Estructuras de Datos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        viz_title.pack(pady=10)

        # Frame para heap y AVL lado a lado
        viz_container = ctk.CTkFrame(self.viz_frame, fg_color="transparent")
        viz_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Panel MaxHeap
        heap_frame = ctk.CTkFrame(viz_container)
        heap_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        heap_label = ctk.CTkLabel(
            heap_frame,
            text="Max-Heap (Arreglo)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        heap_label.pack(pady=5)

        self.heap_viz_textbox = ctk.CTkTextbox(
            heap_frame,
            height=120,
            font=ctk.CTkFont(family="Courier New", size=11)
        )
        self.heap_viz_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Panel AVL Tree (Recorridos + Operaciones)
        avl_frame = ctk.CTkFrame(viz_container)
        avl_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Sub-frame para recorridos
        traversals_subframe = ctk.CTkFrame(avl_frame)
        traversals_subframe.pack(side="left", fill="both", expand=True, padx=(0, 5))

        traversals_label = ctk.CTkLabel(
            traversals_subframe,
            text="Arbol AVL (Recorridos)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        traversals_label.pack(pady=5)

        self.avl_traversals_textbox = ctk.CTkTextbox(
            traversals_subframe,
            height=120,
            font=ctk.CTkFont(family="Courier New", size=10)
        )
        self.avl_traversals_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Sub-frame para operaciones
        operations_subframe = ctk.CTkFrame(avl_frame)
        operations_subframe.pack(side="right", fill="both", expand=True, padx=(5, 0))

        operations_label = ctk.CTkLabel(
            operations_subframe,
            text="Historial de Operaciones",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        operations_label.pack(pady=5)

        self.avl_operations_textbox = ctk.CTkTextbox(
            operations_subframe,
            height=120,
            font=ctk.CTkFont(family="Courier New", size=10)
        )
        self.avl_operations_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _set_date(self, days_offset):
        """Establece la fecha en el campo de entrada"""
        target_date = datetime.now() + timedelta(days=days_offset)
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, target_date.strftime("%Y-%m-%d"))
    
    def _start_drag(self, event):
        """Inicia el arrastre del divisor"""
        self.dragging = True
        self.drag_start_y = event.y_root

    def _on_drag(self, event):
        """Maneja el movimiento del divisor durante el arrastre"""
        if not self.dragging:
            return

        # Calcular el desplazamiento
        delta_y = event.y_root - self.drag_start_y
        self.drag_start_y = event.y_root

        # Actualizar alturas
        new_main_height = self.main_container_height + delta_y
        new_viz_height = self.viz_frame_height - delta_y

        # Límites mínimos y máximos
        min_main_height = 200
        min_viz_height = 150
        max_total_height = 800

        # Verificar límites
        if new_main_height >= min_main_height and new_viz_height >= min_viz_height:
            if (new_main_height + new_viz_height) <= max_total_height:
                self.main_container_height = new_main_height
                self.viz_frame_height = new_viz_height

                # Aplicar nuevas alturas
                self.main_container.configure(height=self.main_container_height)
                self.viz_frame.configure(height=self.viz_frame_height)

    def _stop_drag(self, event):
        """Detiene el arrastre del divisor"""
        self.dragging = False

    def add_task(self):
        """Agrega una nueva tarea al sistema"""
        try:
            # Obtener datos
            description = self.desc_entry.get("1.0", "end").strip()
            priority = self.priority_var.get()
            due_date = self.date_entry.get().strip()

            # Validar fecha
            if not due_date:
                messagebox.showwarning("Advertencia", "Por favor ingrese una fecha de vencimiento")
                return

            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return

            # Agregar tarea
            task = self.controller.add_task(description, priority, due_date)

            # Limpiar campos
            self.desc_entry.delete("1.0", "end")
            self.date_entry.delete(0, 'end')
            self.priority_var.set("MEDIA")

            # Actualizar vista
            self.refresh_task_list()
            self.update_statistics()
            self.update_visualizations()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def complete_highest_priority(self):
        """Completa la tarea con mayor prioridad"""
        task = self.controller.complete_highest_priority_task()

        if task:
            self.refresh_task_list()
            self.update_statistics()
            self.update_visualizations()
            messagebox.showinfo(
                "Tarea Completada",
                f"Tarea completada:\n\n{task}"
            )
        else:
            messagebox.showinfo("Información", "No hay tareas pendientes")

    def search_task(self):
        """Busca una tarea por ID"""
        try:
            task_id = int(self.search_entry.get())
            task = self.controller.search_task_by_id(task_id)

            if task:
                messagebox.showinfo(
                    f"Tarea encontrada (ID: {task_id})",
                    f"{task}\n\nCreada: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            else:
                messagebox.showwarning("No encontrado", f"No existe tarea con ID: {task_id}")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un ID válido (número)")

    def delete_task_by_id(self):
        """Elimina una tarea específica por ID"""
        try:
            task_id = int(self.search_entry.get())

            if messagebox.askyesno("Confirmar", f"¿Eliminar tarea con ID {task_id}?"):
                success = self.controller.delete_task_by_id(task_id)

                if success:
                    self.refresh_task_list()
                    self.update_statistics()
                    self.update_visualizations()
                    self.search_entry.delete(0, 'end')
                    messagebox.showinfo("Éxito", f"Tarea {task_id} eliminada")
                else:
                    messagebox.showwarning("No encontrado", f"No existe tarea con ID: {task_id}")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un ID válido (número)")

    def refresh_task_list(self):
        """Actualiza la lista de tareas en la interfaz"""
        self.tasks_textbox.configure(state="normal")
        self.tasks_textbox.delete("1.0", "end")

        tasks = self.controller.get_all_tasks_by_id()

        if not tasks:
            self.tasks_textbox.insert("end", "\n   No hay tareas registradas\n\n")
        else:
            # Encabezado
            header = f"{'ID':<6} {'Descripción':<40} {'Prioridad':<10} {'Vencimiento':<12}\n"
            separator = "=" * 100 + "\n"

            self.tasks_textbox.insert("end", header)
            self.tasks_textbox.insert("end", separator)

            # Tareas
            for task in tasks:
                desc = task.description[:37] + "..." if len(task.description) > 40 else task.description
                line = f"{task.task_id:<6} {desc:<40} {task.priority_name:<10} {task.due_date:<12}\n"
                self.tasks_textbox.insert("end", line)

        self.tasks_textbox.configure(state="disabled")

    def update_statistics(self):
        """Actualiza las estadísticas mostradas"""
        stats = self.controller.get_statistics()

        # Formato compacto horizontal
        next_task = stats['highest_priority']
        next_desc = 'N/A'
        if next_task:
            next_desc = next_task.description[:40] + '...' if len(next_task.description) > 40 else next_task.description

        stats_text = f"Total: {stats['total']}  |  Alta: {stats['alta']}  |  Media: {stats['media']}  |  Baja: {stats['baja']}\n"
        stats_text += f"Proxima prioritaria: {next_desc}"

        self.stats_label.configure(text=stats_text)

    def update_visualizations(self):
        """Actualiza las visualizaciones del Heap y AVL"""
        # Actualizar visualización del Max-Heap
        heap_repr = self.controller.get_heap_visualization()
        self.heap_viz_textbox.configure(state="normal")
        self.heap_viz_textbox.delete("1.0", "end")
        self.heap_viz_textbox.insert("end", f"Representacion como arreglo:\n{heap_repr}\n\n")
        self.heap_viz_textbox.insert("end", "Formato: (ID:PrioridadFecha)\n")
        self.heap_viz_textbox.insert("end", "Donde: A=Alta, M=Media, B=Baja\n")
        self.heap_viz_textbox.configure(state="disabled")

        # Actualizar recorridos del AVL Tree
        traversals = self.controller.get_avl_traversals()
        avl_stats = self.controller.get_avl_stats()

        self.avl_traversals_textbox.configure(state="normal")
        self.avl_traversals_textbox.delete("1.0", "end")

        # Mostrar recorridos
        if avl_stats['nodos'] > 0:
            self.avl_traversals_textbox.insert("end", "Recorridos del Arbol AVL:\n\n")
            self.avl_traversals_textbox.insert("end", f"Preorden: {traversals['preorden']}\n")
            self.avl_traversals_textbox.insert("end", f"Inorden: {traversals['inorden']}")

            # Verificar si el inorden está ordenado (BST válido)
            if traversals['is_sorted']:
                self.avl_traversals_textbox.insert("end", " ✓\n")
            else:
                self.avl_traversals_textbox.insert("end", " ✗ (ERROR)\n")

            self.avl_traversals_textbox.insert("end", f"Postorden: {traversals['postorden']}\n\n")

            # Estadísticas del árbol
            self.avl_traversals_textbox.insert("end", f"Altura: {avl_stats['altura']}, ")
            self.avl_traversals_textbox.insert("end", f"Nodos: {avl_stats['nodos']}, ")
            self.avl_traversals_textbox.insert("end", f"Balanceado: {'SI' if avl_stats['balanceado'] else 'NO'}\n")
        else:
            # Mensaje limpio si está vacío
            self.avl_traversals_textbox.insert("end", "Arbol vacio")

        self.avl_traversals_textbox.configure(state="disabled")

        # Actualizar historial de operaciones
        operations = self.controller.get_avl_operations(15)

        self.avl_operations_textbox.configure(state="normal")
        self.avl_operations_textbox.delete("1.0", "end")

        if operations:
            self.avl_operations_textbox.insert("end", "Ultimas operaciones:\n\n")
            for i, op in enumerate(operations, 1):
                self.avl_operations_textbox.insert("end", f"{i}. {op}\n")
        else:
            self.avl_operations_textbox.insert("end", "No hay operaciones registradas\n")

        self.avl_operations_textbox.configure(state="disabled")

    def run(self):
        """Inicia el loop principal de la aplicación"""
        self.root.mainloop()