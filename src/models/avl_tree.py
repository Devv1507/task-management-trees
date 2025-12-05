"""
Implementación de Árbol AVL para indexación eficiente de tareas por ID.
Garantiza búsqueda, inserción y eliminación en O(log n).
"""

class AVLNode:
    """Nodo del árbol AVL"""

    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """
    Árbol AVL auto-balanceado para indexar tareas por ID único.
    Mantiene el balance del árbol en cada operación.
    """

    def __init__(self):
        self.root = None
        self.operations = []  # Historial de operaciones (inserciones, eliminaciones, rotaciones)

    def _get_height(self, node):
        """Retorna la altura de un nodo"""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """
        Calcula el factor de balance de un nodo.
        Balance = altura(subárbol izquierdo) - altura(subárbol derecho)
        """
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node):
        """Actualiza la altura de un nodo"""
        if not node:
            return
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _rotate_right(self, z):
        """
        Rotación simple a la derecha
             z                      y
            / \                    / \
           y   C    ------>       x   z
          / \                        / \
         x   B                      B   C
        """
        y = z.left
        B = y.right

        # Registrar operación
        self.operations.append(f"Rotacion Derecha en nodo ID:{z.task.task_id}")

        # Realizar rotación
        y.right = z
        z.left = B

        # Actualizar alturas
        self._update_height(z)
        self._update_height(y)

        return y

    def _rotate_left(self, z):
        """
        Rotación simple a la izquierda
           z                          y
          / \                        / \
         A   y       ------>        z   x
            / \                    / \
           B   x                  A   B
        """
        y = z.right
        B = y.left

        # Registrar operación
        self.operations.append(f"Rotacion Izquierda en nodo ID:{z.task.task_id}")

        # Realizar rotación
        y.left = z
        z.right = B

        # Actualizar alturas
        self._update_height(z)
        self._update_height(y)

        return y

    def _rebalance(self, node):
        """
        Rebalancea el nodo si es necesario después de una inserción o eliminación.
        Detecta y corrige los 4 casos de desbalance.
        """
        # Actualizar altura del nodo actual
        self._update_height(node)

        # Calcular factor de balance
        balance = self._get_balance(node)

        # Caso 1: Desbalance izquierda-izquierda (Left-Left)
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Caso 2: Desbalance izquierda-derecha (Left-Right)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso 3: Desbalance derecha-derecha (Right-Right)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Caso 4: Desbalance derecha-izquierda (Right-Left)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, task):
        """
        Inserta una tarea en el árbol AVL por su ID.
        Complejidad: O(log n)
        """
        self.operations.append(f"Insercion ID:{task.task_id}")
        self.root = self._insert_recursive(self.root, task)

    def _insert_recursive(self, node, task):
        """Inserción recursiva con rebalanceo"""
        # Caso base: insertar en posición vacía
        if not node:
            return AVLNode(task)

        # Insertar en el subárbol correspondiente
        if task.task_id < node.task.task_id:
            node.left = self._insert_recursive(node.left, task)
        elif task.task_id > node.task.task_id:
            node.right = self._insert_recursive(node.right, task)
        else:
            # ID duplicado - actualizar la tarea existente
            node.task = task
            return node

        # Rebalancear el árbol
        return self._rebalance(node)

    def search(self, task_id):
        """
        Busca una tarea por su ID.
        Complejidad: O(log n)
        """
        return self._search_recursive(self.root, task_id)

    def _search_recursive(self, node, task_id):
        """Búsqueda recursiva"""
        # Caso base: nodo vacío o encontrado
        if not node or node.task.task_id == task_id:
            return node.task if node else None

        # Buscar en subárbol izquierdo o derecho
        if task_id < node.task.task_id:
            return self._search_recursive(node.left, task_id)
        else:
            return self._search_recursive(node.right, task_id)

    def delete(self, task_id):
        """
        Elimina una tarea del árbol por su ID.
        Complejidad: O(log n)
        """
        self.operations.append(f"Eliminacion ID:{task_id}")
        self.root = self._delete_recursive(self.root, task_id)

    def _delete_recursive(self, node, task_id):
        """Eliminación recursiva con rebalanceo"""
        # Caso base: nodo no encontrado
        if not node:
            return node

        # Buscar el nodo a eliminar
        if task_id < node.task.task_id:
            node.left = self._delete_recursive(node.left, task_id)
        elif task_id > node.task.task_id:
            node.right = self._delete_recursive(node.right, task_id)
        else:
            # Nodo encontrado - proceder a eliminarlo

            # Caso 1: Nodo sin hijos o con un solo hijo
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Caso 2: Nodo con dos hijos
            # Encontrar el sucesor in-order (mínimo del subárbol derecho)
            successor = self._find_min(node.right)
            node.task = successor.task
            node.right = self._delete_recursive(node.right, successor.task.task_id)

        # Rebalancear el árbol
        return self._rebalance(node)

    def _find_min(self, node):
        """Encuentra el nodo con el valor mínimo (más a la izquierda)"""
        current = node
        while current.left:
            current = current.left
        return current

    def get_all_tasks(self):
        """
        Retorna todas las tareas en orden (in-order traversal).
        Las tareas estarán ordenadas por ID.
        """
        tasks = []
        self._inorder_traversal(self.root, tasks)
        return tasks

    def _inorder_traversal(self, node, tasks):
        """Recorrido in-order recursivo"""
        if node:
            self._inorder_traversal(node.left, tasks)
            tasks.append(node.task)
            self._inorder_traversal(node.right, tasks)

    def is_empty(self):
        """Verifica si el árbol está vacío"""
        return self.root is None

    def size(self):
        """Retorna el número de nodos en el árbol"""
        return self._count_nodes(self.root)

    def _count_nodes(self, node):
        """Cuenta recursivamente los nodos del árbol"""
        if not node:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def get_tree_structure(self):
        """
        Retorna una representación visual simple del árbol AVL.
        Muestra la estructura con indentación.

        Returns:
            str: Representación textual del árbol
        """
        if self.is_empty():
            return "Arbol vacio"

        lines = []
        self._build_tree_string(self.root, "", True, lines)
        return "\n".join(lines)

    def _build_tree_string(self, node, prefix, is_tail, lines):
        """
        Construye recursivamente la representación del árbol.

        Args:
            node: Nodo actual
            prefix: Prefijo para la línea actual
            is_tail: Si es el último hijo
            lines: Lista de líneas de salida
        """
        if node:
            lines.append(prefix + ("└── " if is_tail else "├── ") +
                        f"ID:{node.task.task_id} ({node.task.priority_name[0]}, h={node.height})")

            children = []
            if node.left:
                children.append(node.left)
            if node.right:
                children.append(node.right)

            for i, child in enumerate(children):
                extension = "    " if is_tail else "│   "
                is_last = (i == len(children) - 1)
                self._build_tree_string(child, prefix + extension, is_last, lines)

    def get_tree_stats(self):
        """
        Retorna estadísticas del árbol AVL para verificar balance.

        Returns:
            dict: Diccionario con estadísticas del árbol
        """
        if self.is_empty():
            return {
                'height': 0,
                'nodes': 0,
                'balanced': True,
                'min_height': 0,
                'max_height': 0
            }

        return {
            'height': self.root.height,
            'nodes': self.size(),
            'balanced': self._is_balanced(self.root),
            'balance_factor': self._get_balance(self.root)
        }

    def _is_balanced(self, node):
        """
        Verifica recursivamente si el árbol está balanceado.

        Returns:
            bool: True si el árbol está balanceado
        """
        if not node:
            return True

        balance = self._get_balance(node)
        if abs(balance) > 1:
            return False

        return self._is_balanced(node.left) and self._is_balanced(node.right)

