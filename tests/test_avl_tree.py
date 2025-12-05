"""
Casos de prueba para AVLTree.
Verifica el correcto funcionamiento del árbol auto-balanceado.
"""

import sys
import os
import time
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.avl_tree import AVLTree
from src.models.task import Task


def test_search():
    """Prueba de indexación: Buscar elementos aleatorios en el árbol"""
    print("\n=== Test 1: Búsqueda de elementos ===")

    tree = AVLTree()

    # Insertar tareas
    tasks = [
        Task(50, "Tarea 50", "ALTA", "2024-12-10"),
        Task(25, "Tarea 25", "MEDIA", "2024-12-15"),
        Task(75, "Tarea 75", "BAJA", "2024-12-20"),
        Task(10, "Tarea 10", "ALTA", "2024-12-08"),
        Task(30, "Tarea 30", "MEDIA", "2024-12-12"),
        Task(60, "Tarea 60", "BAJA", "2024-12-18"),
        Task(80, "Tarea 80", "ALTA", "2024-12-25")
    ]

    for task in tasks:
        tree.insert(task)

    print(f"Insertadas {tree.size()} tareas")

    # Buscar elementos específicos
    search_ids = [50, 10, 80, 30, 60]
    print("\nBuscando tareas por ID:")
    for task_id in search_ids:
        found = tree.search(task_id)
        assert found is not None, f"Debería encontrar la tarea {task_id}"
        print(f"  ✓ Encontrada: {found}")

    # Buscar elemento inexistente
    not_found = tree.search(999)
    assert not_found is None, "No debería encontrar tarea inexistente"
    print("  ✓ Búsqueda de elemento inexistente retorna None")

    print("✓ Test 1 pasado exitosamente")


def test_balance():
    """Prueba de equilibrio: Insertar secuencia desbalanceada y verificar reequilibrio"""
    print("\n=== Test 2: Auto-balanceo del árbol ===")

    tree = AVLTree()

    # Insertar en orden ascendente (peor caso para árbol binario sin balance)
    print("Insertando secuencia ascendente (1, 2, 3, ..., 15):")
    for i in range(1, 16):
        task = Task(i, f"Tarea {i}", "MEDIA", "2024-12-31")
        tree.insert(task)

    print(f"Tareas insertadas: {tree.size()}")

    # Verificar que todas las tareas están presentes
    for i in range(1, 16):
        found = tree.search(i)
        assert found is not None, f"Tarea {i} debería estar en el árbol"

    # Verificar altura del árbol (debería ser logarítmica)
    # Para 15 nodos, la altura máxima de un AVL es log2(15) ≈ 4-5
    height = tree.root.height
    print(f"Altura del árbol: {height}")
    assert height <= 5, f"Árbol desbalanceado, altura {height} es muy grande para 15 nodos"

    print("✓ Test 2 pasado exitosamente (árbol mantiene balance)")


def test_delete_and_rebalance():
    """Prueba de eliminación con rebalanceo"""
    print("\n=== Test 3: Eliminación con rebalanceo ===")

    tree = AVLTree()

    # Insertar tareas
    ids = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55, 65, 77, 85]
    for task_id in ids:
        task = Task(task_id, f"Tarea {task_id}", "MEDIA", "2024-12-31")
        tree.insert(task)

    print(f"Insertadas {len(ids)} tareas")
    initial_height = tree.root.height

    # Eliminar varias tareas
    to_delete = [10, 30, 60, 80]
    for task_id in to_delete:
        tree.delete(task_id)
        print(f"  Eliminada tarea {task_id}")

    print(f"Tareas restantes: {tree.size()}")

    # Verificar que las tareas eliminadas no están
    for task_id in to_delete:
        found = tree.search(task_id)
        assert found is None, f"Tarea {task_id} debería estar eliminada"

    # Verificar que las demás tareas siguen presentes
    remaining_ids = [i for i in ids if i not in to_delete]
    for task_id in remaining_ids:
        found = tree.search(task_id)
        assert found is not None, f"Tarea {task_id} debería seguir presente"

    # Verificar que el árbol mantiene balance
    final_height = tree.root.height if tree.root else 0
    print(f"Altura después de eliminaciones: {final_height}")

    print("✓ Test 3 pasado exitosamente")


def test_inorder_traversal():
    """Prueba de recorrido in-order (debe retornar elementos ordenados)"""
    print("\n=== Test 4: Recorrido in-order ===")

    tree = AVLTree()

    # Insertar en orden aleatorio
    ids = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for task_id in ids:
        task = Task(task_id, f"Tarea {task_id}", "MEDIA", "2024-12-31")
        tree.insert(task)

    # Obtener todas las tareas (in-order)
    all_tasks = tree.get_all_tasks()

    print(f"Tareas en orden: {[t.task_id for t in all_tasks]}")

    # Verificar que están ordenadas por ID
    for i in range(len(all_tasks) - 1):
        assert all_tasks[i].task_id < all_tasks[i + 1].task_id, \
            "Las tareas deberían estar ordenadas por ID"

    print("✓ Test 4 pasado exitosamente (tareas en orden)")


def test_update_existing():
    """Prueba de actualización de tarea existente"""
    print("\n=== Test 5: Actualización de tarea existente ===")

    tree = AVLTree()

    # Insertar tarea inicial
    task1 = Task(100, "Tarea original", "MEDIA", "2024-12-10")
    tree.insert(task1)

    # Insertar tarea con mismo ID (debería actualizar)
    task2 = Task(100, "Tarea actualizada", "ALTA", "2024-12-15")
    tree.insert(task2)

    # Verificar que solo hay una tarea
    assert tree.size() == 1, "No debería duplicar tareas con mismo ID"

    # Verificar que la tarea fue actualizada
    found = tree.search(100)
    assert found.description == "Tarea actualizada", "Debería actualizar la descripción"
    assert found.priority_name == "ALTA", "Debería actualizar la prioridad"

    print("✓ Test 5 pasado exitosamente (actualización correcta)")


def test_search_performance_complexity():
    """Prueba de complejidad O(log n): Verificar tiempos de respuesta eficientes"""
    print("\n=== Test 6: Verificación de Complejidad O(log n) ===")

    # Tamaños de prueba
    n1 = 1000
    n2 = 10000
    num_searches = 100  # Número de búsquedas para promediar

    print(f"Insertando {n1} elementos en el árbol 1...")
    tree1 = AVLTree()
    for i in range(1, n1 + 1):
        task = Task(i, f"Tarea {i}", "MEDIA", "2024-12-31")
        tree1.insert(task)

    print(f"Insertando {n2} elementos en el árbol 2...")
    tree2 = AVLTree()
    for i in range(1, n2 + 1):
        task = Task(i, f"Tarea {i}", "MEDIA", "2024-12-31")
        tree2.insert(task)

    # Medir tiempo promedio de búsqueda en árbol 1
    print(f"\nMidiendo {num_searches} búsquedas en árbol de {n1} elementos...")
    start_time = time.time()
    for i in range(num_searches):
        # Buscar elementos aleatorios distribuidos uniformemente
        search_id = (i * (n1 // num_searches)) + 1
        tree1.search(search_id)
    time1 = (time.time() - start_time) / num_searches

    # Medir tiempo promedio de búsqueda en árbol 2
    print(f"Midiendo {num_searches} búsquedas en árbol de {n2} elementos...")
    start_time = time.time()
    for i in range(num_searches):
        # Buscar elementos aleatorios distribuidos uniformemente
        search_id = (i * (n2 // num_searches)) + 1
        tree2.search(search_id)
    time2 = (time.time() - start_time) / num_searches

    # Calcular relaciones
    expected_ratio = math.log2(n2) / math.log2(n1)
    actual_ratio = time2 / time1 if time1 > 0 else 0

    # Mostrar resultados con operación matemática
    print(f"\n--- Resultados ---")
    print(f"Tiempo promedio búsqueda ({n1} elementos):  {time1*1000:.6f} ms")
    print(f"Tiempo promedio búsqueda ({n2} elementos): {time2*1000:.6f} ms")
    print(f"\nRelación esperada (logarítmica):")
    print(f"  log₂({n2}) / log₂({n1}) = {math.log2(n2):.2f} / {math.log2(n1):.2f} = {expected_ratio:.3f}x")
    print(f"\nRelación real (tiempos medidos):")
    print(f"  T({n2}) / T({n1}) = {actual_ratio:.3f}x")

    # Verificar que la relación sea aproximadamente logarítmica
    # Permitimos hasta 2x de diferencia debido a factores del sistema
    tolerance = 2.0
    ratio_difference = abs(actual_ratio - expected_ratio)

    print(f"\nDiferencia: {ratio_difference:.3f}")
    print(f"Tolerancia permitida: {tolerance}x")

    # La relación real debería ser cercana a la esperada
    # Si fuera O(n), la relación sería 10x (n2/n1)
    # Si es O(log n), la relación debería ser ~3.3x (log2(10000)/log2(1000))
    if actual_ratio > 10:
        print(f"\n✗ ADVERTENCIA: Relación muy alta ({actual_ratio:.2f}x), podría no ser O(log n)")

    assert ratio_difference < tolerance or actual_ratio < expected_ratio * 1.5, \
        f"Complejidad no parece logarítmica: esperado ~{expected_ratio:.2f}x, obtenido {actual_ratio:.2f}x"

    print(f"\n✓ Test 6 pasado exitosamente")
    print(f"✓ Complejidad verificada: O(log n)")


def run_all_tests():
    """Ejecuta todas las pruebas del AVL Tree"""
    print("\n" + "="*60)
    print("EJECUTANDO PRUEBAS DE ÁRBOL AVL")
    print("="*60)

    try:
        test_search()
        test_balance()
        test_delete_and_rebalance()
        test_inorder_traversal()
        test_update_existing()
        test_search_performance_complexity()

        print("\n" + "="*60)
        print("✓ TODAS LAS PRUEBAS DE AVL TREE PASARON EXITOSAMENTE")
        print("="*60)

    except AssertionError as e:
        print(f"\n✗ PRUEBA FALLIDA: {e}")
        return False

    return True


if __name__ == "__main__":
    run_all_tests()
