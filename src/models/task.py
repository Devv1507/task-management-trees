"""
Modelo de datos para representar una tarea en el sistema.
"""

from datetime import datetime
from enum import Enum


class Priority(Enum):
    """Enumeración de prioridades de tareas"""
    BAJA = 1
    MEDIA = 2
    ALTA = 3


class Task:
    """
    Representa una tarea en el sistema de gestión de productividad.

    Atributos:
        task_id (int): Identificador único de la tarea
        description (str): Descripción de la tarea
        priority (int): Prioridad numérica (1=Baja, 2=Media, 3=Alta)
        priority_name (str): Nombre de la prioridad (Baja, Media, Alta)
        due_date (str): Fecha de vencimiento en formato YYYY-MM-DD
        created_at (datetime): Fecha y hora de creación
    """

    def __init__(self, task_id, description, priority_name, due_date):
        """
        Inicializa una nueva tarea.

        Args:
            task_id (int): ID único de la tarea
            description (str): Descripción de la tarea
            priority_name (str): Prioridad ('BAJA', 'MEDIA', 'ALTA')
            due_date (str): Fecha de vencimiento (YYYY-MM-DD)
        """
        self.task_id = task_id
        self.description = description
        self.priority_name = priority_name.upper()
        self.priority = self._get_priority_value(self.priority_name)
        self.due_date = due_date
        self.created_at = datetime.now()

    def _get_priority_value(self, priority_name):
        """
        Convierte el nombre de prioridad a su valor numérico.

        Args:
            priority_name (str): Nombre de la prioridad

        Returns:
            int: Valor numérico de la prioridad (1, 2, o 3)
        """
        priority_map = {
            'BAJA': Priority.BAJA.value,
            'MEDIA': Priority.MEDIA.value,
            'ALTA': Priority.ALTA.value
        }
        return priority_map.get(priority_name, Priority.MEDIA.value)

    def __str__(self):
        """Representación en string de la tarea"""
        return f"[ID: {self.task_id}] {self.description} | Prioridad: {self.priority_name} | Vence: {self.due_date}"

    def __repr__(self):
        """Representación técnica de la tarea"""
        return f"Task(id={self.task_id}, desc='{self.description}', priority={self.priority_name})"

    def __eq__(self, other):
        """Compara dos tareas por su ID"""
        if not isinstance(other, Task):
            return False
        return self.task_id == other.task_id

    def __lt__(self, other):
        """
        Comparación para ordenamiento.
        Primero por prioridad (descendente), luego por fecha de vencimiento (ascendente)
        """
        if not isinstance(other, Task):
            return NotImplemented

        if self.priority != other.priority:
            return self.priority > other.priority  # Mayor prioridad primero

        return self.due_date < other.due_date  # Fecha más cercana primero

    def to_dict(self):
        """
        Convierte la tarea a un diccionario.

        Returns:
            dict: Diccionario con los datos de la tarea
        """
        return {
            'task_id': self.task_id,
            'description': self.description,
            'priority': self.priority,
            'priority_name': self.priority_name,
            'due_date': self.due_date,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def get_priority_color(priority_name):
        """
        Retorna el color asociado a una prioridad para la UI.

        Args:
            priority_name (str): Nombre de la prioridad

        Returns:
            str: Código de color hexadecimal
        """
        color_map = {
            'BAJA': '#4CAF50',    # Verde
            'MEDIA': '#FF9800',   # Naranja
            'ALTA': '#F44336'     # Rojo
        }
        return color_map.get(priority_name.upper(), '#808080')  # Gris por defecto
