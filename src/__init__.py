"""
Sistema de Gestión de Tareas.
Un sistema de productividad que utiliza árboles AVL y heaps para gestionar tareas con prioridades.
"""
from .task import Task, Priority
from .avl_tree import AVLTree
from .min_heap import MinHeap
from .task_manager import TaskManager

__all__ = ['Task', 'Priority', 'AVLTree', 'MinHeap', 'TaskManager']

__version__ = '1.0.0'