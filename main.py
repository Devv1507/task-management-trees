"""
Punto de entrada principal de la aplicación.
Sistema de Gestión de Tareas con Colas de Prioridad y Árboles AVL.
"""

import sys
from src.controllers.task_controller import TaskController
from src.views.main_window import MainWindow


def main():
    """
    Función principal que inicializa y ejecuta la aplicación.
    """
    try:
        # Crear controlador
        controller = TaskController()

        # Crear y mostrar la ventana principal
        app = MainWindow(controller)

        # Iniciar la aplicación
        app.run()

    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
