"""
Ejecuta todas las pruebas del sistema.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_max_heap import run_all_tests as test_heap
from tests.test_avl_tree import run_all_tests as test_avl


def main():
    """Ejecuta todas las pruebas del sistema"""
    print("\n" + "="*70)
    print(" SUITE COMPLETA DE PRUEBAS - SISTEMA DE GESTIÓN DE TAREAS")
    print("="*70)

    # Ejecutar pruebas del MaxHeap
    heap_passed = test_heap()

    print("\n")

    # Ejecutar pruebas del AVL Tree
    avl_passed = test_avl()

    # Resumen final
    print("\n" + "="*70)
    print(" RESUMEN FINAL")
    print("="*70)
    print(f"Max-Heap: {'✓ PASADO' if heap_passed else '✗ FALLADO'}")
    print(f"AVL Tree: {'✓ PASADO' if avl_passed else '✗ FALLADO'}")

    if heap_passed and avl_passed:
        print("\nTODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*70)
        return 0
    else:
        print("\nALGUNAS PRUEBAS FALLARON")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
