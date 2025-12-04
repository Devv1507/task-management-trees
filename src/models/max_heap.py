"""
Implementación de Max-Heap para gestionar cola de prioridad de tareas.
El elemento con mayor prioridad siempre estará en la raíz.
"""

class MaxHeap:
    """
    Max-Heap binario para gestionar tareas por prioridad.
    Prioridad: Alta=3, Media=2, Baja=1
    """

    def __init__(self):
        self.heap = []

    def _parent(self, index):
        """Retorna el índice del padre"""
        return (index - 1) // 2

    def _left_child(self, index):
        """Retorna el índice del hijo izquierdo"""
        return 2 * index + 1

    def _right_child(self, index):
        """Retorna el índice del hijo derecho"""
        return 2 * index + 2

    def _swap(self, i, j):
        """Intercambia dos elementos en el heap"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index):
        """
        Mantiene la propiedad del max-heap moviendo el elemento hacia arriba.
        Se ejecuta después de insertar un nuevo elemento.
        """
        parent = self._parent(index)

        # Mientras no sea la raíz y el elemento sea mayor que su padre
        if index > 0 and self.heap[index].priority > self.heap[parent].priority:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        """
        Mantiene la propiedad del max-heap moviendo el elemento hacia abajo.
        Se ejecuta después de extraer el elemento máximo.
        """
        largest = index
        left = self._left_child(index)
        right = self._right_child(index)

        # Encontrar el mayor entre el nodo actual y sus hijos
        if left < len(self.heap) and self.heap[left].priority > self.heap[largest].priority:
            largest = left

        if right < len(self.heap) and self.heap[right].priority > self.heap[largest].priority:
            largest = right

        # Si el mayor no es el nodo actual, intercambiar y continuar
        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

    def insert(self, task):
        """
        Inserta una nueva tarea en el heap.
        Complejidad: O(log n)
        """
        self.heap.append(task)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        """
        Extrae y retorna la tarea con mayor prioridad.
        Complejidad: O(log n)
        """
        if self.is_empty():
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        # Guardar el máximo
        max_task = self.heap[0]

        # Mover el último elemento a la raíz
        self.heap[0] = self.heap.pop()

        # Reequilibrar el heap
        self._heapify_down(0)

        return max_task

    def peek(self):
        """
        Retorna la tarea con mayor prioridad sin extraerla.
        Complejidad: O(1)
        """
        return self.heap[0] if not self.is_empty() else None

    def remove(self, task_id):
        """
        Elimina una tarea específica del heap por su ID.
        Complejidad: O(n) para buscar + O(log n) para reequilibrar
        """
        # Buscar el índice de la tarea
        index = -1
        for i, task in enumerate(self.heap):
            if task.task_id == task_id:
                index = i
                break

        if index == -1:
            return False  # Tarea no encontrada

        # Si es el último elemento, simplemente eliminarlo
        if index == len(self.heap) - 1:
            self.heap.pop()
            return True

        # Reemplazar con el último elemento
        self.heap[index] = self.heap.pop()

        # Reequilibrar (puede necesitar subir o bajar)
        parent = self._parent(index)
        if index > 0 and self.heap[index].priority > self.heap[parent].priority:
            self._heapify_up(index)
        else:
            self._heapify_down(index)

        return True

    def is_empty(self):
        """Verifica si el heap está vacío"""
        return len(self.heap) == 0

    def size(self):
        """Retorna el número de elementos en el heap"""
        return len(self.heap)

    def get_all_tasks(self):
        """Retorna todas las tareas en el heap (sin orden específico)"""
        return self.heap.copy()
