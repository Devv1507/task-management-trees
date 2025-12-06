import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.max_heap import MaxHeap
from src.models.task import Task

"""
Casos de prueba para MaxHeap.
Verifica el correcto funcionamiento de la cola de prioridad.
"""
def test_insert_and_extract():
    """Prueba de inserción: Ingresar múltiples tareas con diferentes prioridades"""
    print("\n=== Test 1: Inserción y extracción por prioridad ===")

    heap = MaxHeap()

    # Crear tareas con diferentes prioridades
    task1 = Task(101, "Estudiar para el examen", "ALTA", "2024-12-10")
    task2 = Task(102, "Comprar útiles escolares", "MEDIA", "2024-12-15")
    task3 = Task(103, "Revisar correos electrónicos", "BAJA", "2024-12-20")
    task4 = Task(104, "Presentación del proyecto", "ALTA", "2024-12-08")
    task5 = Task(105, "Limpiar escritorio", "BAJA", "2024-12-25")

    # Insertar tareas
    heap.insert(task1)
    heap.insert(task2)
    heap.insert(task3)
    heap.insert(task4)
    heap.insert(task5)

    print(f"Tareas insertadas: {heap.size()}")

    # Extraer en orden de prioridad
    print("\nOrden de extracción (debe ser por prioridad ALTA -> MEDIA -> BAJA):")
    order = []
    while not heap.is_empty():
        task = heap.extract_max()
        order.append(task.task_id)
        print(f"  - {task}")

    # Verificar orden: deberían salir las tareas de alta prioridad primero
    # IDs 101 y 104 son ALTA, 102 es MEDIA, 103 y 105 son BAJA
    assert order[0] in [101, 104], "Primera tarea debería ser ALTA prioridad"
    assert order[1] in [101, 104], "Segunda tarea debería ser ALTA prioridad"
    assert order[2] == 102, "Tercera tarea debería ser MEDIA prioridad"
    assert order[3] in [103, 105], "Cuarta tarea debería ser BAJA prioridad"
    assert order[4] in [103, 105], "Quinta tarea debería ser BAJA prioridad"

    print("✓ Test 1 pasado exitosamente")


def test_heap_property():
    """Prueba de eliminación: Verificar que la estructura del heap se mantiene"""
    print("\n=== Test 2: Mantenimiento de propiedad del heap ===")

    heap = MaxHeap()

    # Insertar varias tareas
    for i in range(1, 11):
        priority = ["BAJA", "MEDIA", "ALTA"][i % 3]
        task = Task(i, f"Tarea {i}", priority, "2024-12-31")
        heap.insert(task)

    print(f"Insertadas {heap.size()} tareas")

    # Extraer la mitad
    extracted = []
    for _ in range(5):
        task = heap.extract_max()
        extracted.append(task)

    print(f"Extraídas {len(extracted)} tareas")
    print(f"Tareas restantes: {heap.size()}")

    # Verificar que la prioridad máxima restante es menor o igual a la última extraída
    if not heap.is_empty():
        remaining_max = heap.peek()
        last_extracted = extracted[-1]
        assert remaining_max.priority <= last_extracted.priority, \
            "La propiedad del heap se rompió"

    print("✓ Test 2 pasado exitosamente")


def test_remove_specific_task():
    """Prueba de eliminación específica por ID"""
    print("\n=== Test 3: Eliminación específica de tarea ===")

    heap = MaxHeap()

    # Insertar tareas
    tasks = [
        Task(1, "Tarea 1", "ALTA", "2024-12-10"),
        Task(2, "Tarea 2", "MEDIA", "2024-12-15"),
        Task(3, "Tarea 3", "ALTA", "2024-12-12"),
        Task(4, "Tarea 4", "BAJA", "2024-12-20")
    ]

    for task in tasks:
        heap.insert(task)

    print(f"Tareas insertadas: {heap.size()}")

    # Eliminar tarea con ID 2
    success = heap.remove(2)
    assert success, "Debería eliminar la tarea correctamente"
    print(f"Tarea con ID 2 eliminada. Tareas restantes: {heap.size()}")

    # Verificar que no se puede encontrar
    remaining = heap.get_all_tasks()
    assert not any(t.task_id == 2 for t in remaining), "La tarea 2 no debería estar"

    # Verificar que las demás tareas siguen ahí
    assert heap.size() == 3, "Deberían quedar 3 tareas"

    print("✓ Test 3 pasado exitosamente")


def test_peek():
    """Prueba de peek sin modificar el heap"""
    print("\n=== Test 4: Peek sin modificar ===")

    heap = MaxHeap()

    task1 = Task(1, "Tarea prioritaria", "ALTA", "2024-12-10")
    task2 = Task(2, "Tarea normal", "MEDIA", "2024-12-15")

    heap.insert(task2)
    heap.insert(task1)

    # Peek no debería cambiar el tamaño
    peeked = heap.peek()
    assert heap.size() == 2, "Peek no debería modificar el tamaño"
    assert peeked.task_id == 1, "Peek debería retornar la tarea de mayor prioridad"

    print(f"Tarea con mayor prioridad (sin extraer): {peeked}")
    print("✓ Test 4 pasado exitosamente")


def run_all_tests():
    """Ejecuta todas las pruebas del MaxHeap"""
    print("\n" + "="*60)
    print("EJECUTANDO PRUEBAS DE MAX-HEAP")
    print("="*60)

    try:
        test_insert_and_extract()
        test_heap_property()
        test_remove_specific_task()
        test_peek()

        print("\n" + "="*60)
        print("✓ TODAS LAS PRUEBAS DE MAX-HEAP PASARON EXITOSAMENTE")
        print("="*60)

    except AssertionError as e:
        print(f"\n✗ PRUEBA FALLIDA: {e}")
        return False

    return True


if __name__ == "__main__":
    run_all_tests()
