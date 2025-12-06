from src.models.max_heap import MaxHeap
from src.models.avl_tree import AVLTree
from src.models.task import Task

class TaskController:
    """
    Controlador que gestiona las operaciones sobre tareas.
    Mantiene sincronizadas ambas estructuras de datos (MaxHeap y AVLTree).
    """

    def __init__(self):
        """Inicializa el controlador con las estructuras de datos vacías"""
        self.max_heap = MaxHeap()  # Para gestión de prioridades
        self.avl_tree = AVLTree()  # Para indexación por ID
        self.next_id = 1  # Generador de IDs únicos

    def add_task(self, description, priority_name, due_date):
        """
        Agrega una nueva tarea al sistema.

        Args:
            description (str): Descripción de la tarea
            priority_name (str): Prioridad ('BAJA', 'MEDIA', 'ALTA')
            due_date (str): Fecha de vencimiento (YYYY-MM-DD)

        Returns:
            Task: La tarea creada

        Complejidad: O(log n) para ambas estructuras
        """
        # Validar datos de entrada
        if not description or not description.strip():
            raise ValueError("La descripción no puede estar vacía")

        if priority_name.upper() not in ['BAJA', 'MEDIA', 'ALTA']:
            raise ValueError("Prioridad inválida. Use: BAJA, MEDIA o ALTA")

        # Crear la tarea
        task = Task(self.next_id, description.strip(), priority_name, due_date)
        self.next_id += 1

        # Insertar en ambas estructuras
        self.max_heap.insert(task)
        self.avl_tree.insert(task)

        return task

    def complete_highest_priority_task(self):
        """
        Completa (elimina) la tarea con mayor prioridad.

        Returns:
            Task: La tarea completada o None si no hay tareas

        Complejidad: O(log n)
        """
        # Extraer del heap
        task = self.max_heap.extract_max()

        if task:
            # Eliminar del árbol AVL
            self.avl_tree.delete(task.task_id)

        return task

    def get_highest_priority_task(self):
        """
        Obtiene la tarea con mayor prioridad sin eliminarla.

        Returns:
            Task: La tarea con mayor prioridad o None si no hay tareas

        Complejidad: O(1)
        """
        return self.max_heap.peek()

    def search_task_by_id(self, task_id):
        """
        Busca una tarea específica por su ID.

        Args:
            task_id (int): ID de la tarea a buscar

        Returns:
            Task: La tarea encontrada o None si no existe

        Complejidad: O(log n)
        """
        return self.avl_tree.search(task_id)

    def delete_task_by_id(self, task_id):
        """
        Elimina una tarea específica por su ID.

        Args:
            task_id (int): ID de la tarea a eliminar

        Returns:
            bool: True si se eliminó exitosamente, False si no existe

        Complejidad: O(n) para el heap + O(log n) para el AVL
        """
        # Verificar que la tarea existe
        task = self.avl_tree.search(task_id)
        if not task:
            return False

        # Eliminar de ambas estructuras
        self.max_heap.remove(task_id)
        self.avl_tree.delete(task_id)

        return True

    def get_all_tasks_by_priority(self):
        """
        Obtiene todas las tareas sin orden específico (del heap).

        Returns:
            list: Lista de tareas

        Complejidad: O(n)
        """
        return self.max_heap.get_all_tasks()

    def get_all_tasks_by_id(self):
        """
        Obtiene todas las tareas ordenadas por ID (del AVL).

        Returns:
            list: Lista de tareas ordenadas por ID

        Complejidad: O(n)
        """
        return self.avl_tree.get_all_tasks()

    def get_task_count(self):
        """
        Retorna el número total de tareas en el sistema.

        Returns:
            int: Cantidad de tareas

        Complejidad: O(1)
        """
        return self.max_heap.size()

    def is_empty(self):
        """
        Verifica si el sistema tiene tareas.

        Returns:
            bool: True si no hay tareas, False en caso contrario

        Complejidad: O(1)
        """
        return self.max_heap.is_empty()

    def get_statistics(self):
        """
        Obtiene estadísticas del sistema de tareas.

        Returns:
            dict: Diccionario con estadísticas

        Complejidad: O(n)
        """
        tasks = self.get_all_tasks_by_id()

        if not tasks:
            return {
                'total': 0,
                'alta': 0,
                'media': 0,
                'baja': 0,
                'highest_priority': None
            }

        # Contar por prioridad
        priority_count = {'ALTA': 0, 'MEDIA': 0, 'BAJA': 0}
        for task in tasks:
            priority_count[task.priority_name] += 1

        return {
            'total': len(tasks),
            'alta': priority_count['ALTA'],
            'media': priority_count['MEDIA'],
            'baja': priority_count['BAJA'],
            'highest_priority': self.get_highest_priority_task()
        }

    def clear_all_tasks(self):
        """
        Elimina todas las tareas del sistema.

        Complejidad: O(1)
        """
        self.max_heap = MaxHeap()
        self.avl_tree = AVLTree()

    def get_heap_visualization(self):
        """
        Obtiene la representación visual del Max-Heap.

        Returns:
            str: Representación del heap como arreglo
        """
        return self.max_heap.get_heap_representation()

    def get_avl_traversals(self):
        """
        Obtiene los tres recorridos del Árbol AVL.

        Returns:
            dict: Diccionario con preorden, inorden y postorden
        """
        return {
            'preorden': self.avl_tree.get_preorder(),
            'inorden': self.avl_tree.get_inorder(),
            'postorden': self.avl_tree.get_postorder(),
            'is_sorted': self.avl_tree.is_inorder_sorted()
        }

    def get_avl_operations(self, count=10):
        """
        Obtiene las últimas operaciones realizadas en el AVL.

        Args:
            count (int): Número de operaciones a retornar

        Returns:
            list: Lista de operaciones recientes
        """
        return self.avl_tree.get_recent_operations(count)

    def get_avl_stats(self):
        """
        Obtiene estadísticas del árbol AVL.
        Returns:
            dict: Diccionario con altura, nodos y estado de balance
        """
        height = self.avl_tree.root.height if self.avl_tree.root else 0
        nodes = self.avl_tree.size()
        balanced = self.avl_tree.is_balanced()    
        return {
            'altura': height,
            'nodos': nodes,
            'balanceado': balanced
        }
