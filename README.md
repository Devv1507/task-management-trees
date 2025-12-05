# Sistema de Gestion de Tareas con Colas de Prioridad y Arboles AVL

## Descripcion del Proyecto

Sistema de gestion de tareas que implementa **arquitectura MVC** e integra dos estructuras de datos avanzadas:

- **Max-Heap (Monticulo Binario)**: Gestiona la cola de prioridad de tareas
- **Arbol AVL**: Indexa tareas por ID unico para busquedas eficientes

Este proyecto academico demuestra la implementacion y aplicacion practica de estructuras de datos fundamentales en ciencias de la computacion.

## Caracteristicas Principales

### Estructuras de Datos

#### 1. Max-Heap (Cola de Prioridad)
- Insercion de tareas: O(log n)
- Extraccion de tarea prioritaria: O(log n)
- Consulta de tarea prioritaria: O(1)
- Eliminacion especifica: O(n)
- Mantiene automaticamente la propiedad del heap

#### 2. Arbol AVL (Indexacion)
- Insercion con auto-balanceo: O(log n)
- Busqueda por ID: O(log n)
- Eliminacion con rebalanceo: O(log n)
- Recorrido in-order ordenado: O(n)
- Garantiza altura logaritmica

### Funcionalidades del Sistema

- **Agregar tareas** con descripcion, prioridad y fecha de vencimiento
- **Completar tarea prioritaria** (extrae la de mayor prioridad)
- **Buscar tareas por ID** (busqueda eficiente en O(log n))
- **Eliminar tareas especificas** por ID
- **Estadisticas en tiempo real** (total, por prioridad)
- **Visualizacion de todas las tareas** ordenadas

## Requisitos del Sistema

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS o Linux
- **Dependencias**: Ver `requirements.txt`

## Instalacion

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd temporal-repository
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv env ## o python3

# Activar en Windows
env\Scripts\activate

# Activar en macOS/Linux
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```


## Ejecucion

### Ejecutar pruebas


### Ejecutar la aplicacion

```bash
python main.py ## o python 3
```

```bash
# Pruebas de AVL Tree
python tests/test_avl_tree.py ## o python 3
```
