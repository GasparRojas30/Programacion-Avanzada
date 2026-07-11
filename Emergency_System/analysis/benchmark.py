from __future__ import annotations

import os
import random
import sys
import time
from datetime import datetime

# Soporta ejecucion como modulo (-m) o directa.
if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Emergency_System.data.loaders import load_incidents, load_network, load_centers
from Emergency_System.structures.hash_table import HashTable
from Emergency_System.structures.priority_queue import PriorityQueue
from Emergency_System.structures.sorting import merge_sort, quick_sort, contar_por_zona
from Emergency_System.algorithms.pathfinding import bfs, ucs, a_star


AHORA = datetime(2026, 7, 11, 12, 0, 0)


def _timeit(fn, *args, repeticiones: int = 1):
    """Retorna (resultado, tiempo_promedio_segundos)."""
    mejor = None
    total = 0.0
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        mejor = fn(*args)
        total += time.perf_counter() - t0
    return mejor, total / repeticiones


def sep(titulo: str) -> None:
    print("\n" + "=" * 64)
    print(titulo)
    print("=" * 64)


# ---------------------------------------------------------------------- #
# 1. Sorting: MergeSort vs QuickSort
# ---------------------------------------------------------------------- #
def bench_sorting(incidentes) -> None:
    sep("PARTE 4 - SORTING: MergeSort vs QuickSort")
    key_prioridad = lambda inc: inc.score(AHORA)
    key_tiempo = lambda inc: inc.timestamp

    for etiqueta, key in [("por prioridad (score)", key_prioridad),
                          ("por antiguedad (timestamp)", key_tiempo)]:
        _, t_merge = _timeit(lambda: merge_sort(incidentes, key=key), repeticiones=5)
        _, t_quick = _timeit(lambda: quick_sort(incidentes, key=key), repeticiones=5)
        print(f"\nOrden {etiqueta}  (n={len(incidentes)})")
        print(f"  MergeSort : {t_merge * 1000:8.3f} ms")
        print(f"  QuickSort : {t_quick * 1000:8.3f} ms")

    # Caso adverso para QuickSort: datos ya ordenados.
    ordenados = merge_sort(incidentes, key=key_tiempo)
    _, t_m = _timeit(lambda: merge_sort(ordenados, key=key_tiempo), repeticiones=5)
    _, t_q = _timeit(lambda: quick_sort(ordenados, key=key_tiempo), repeticiones=5)
    print("\nDatos ya ordenados (peor caso clasico de QuickSort)")
    print(f"  MergeSort : {t_m * 1000:8.3f} ms")
    print(f"  QuickSort : {t_q * 1000:8.3f} ms  (mediana-de-tres mitiga el O(n^2))")

    # Verificacion de correctitud (se comparan las CLAVES ordenadas; QuickSort
    # no es estable, por lo que los empates pueden quedar en distinto orden
    # relativo, pero la secuencia de claves debe ser identica a sorted()).
    esperado = [key_tiempo(i) for i in sorted(incidentes, key=key_tiempo)]
    assert [key_tiempo(i) for i in merge_sort(incidentes, key=key_tiempo)] == esperado
    assert [key_tiempo(i) for i in quick_sort(incidentes, key=key_tiempo)] == esperado
    print("\n  Correctitud verificada contra sorted() de Python. OK")


# ---------------------------------------------------------------------- #
# 2. Hash Table: metricas y tiempos
# ---------------------------------------------------------------------- #
def bench_hash(incidentes) -> None:
    sep("PARTE 2 - TABLA HASH: metricas y rendimiento")
    ht = HashTable()
    _, t_ins = _timeit(lambda: [ht.insert(i.id, i) for i in incidentes])
    print(f"\nInsercion de {len(incidentes)} incidentes: {t_ins * 1000:.3f} ms")

    # Busquedas.
    ids = [i.id for i in incidentes]
    t0 = time.perf_counter()
    for _id in ids:
        ht.search(_id)
    t_busq = time.perf_counter() - t0
    print(f"Busqueda de {len(ids)} claves       : {t_busq * 1000:.3f} ms")

    st = ht.stats()
    print("\nMetricas de la tabla hash:")
    for k, v in st.items():
        print(f"  {k:20s}: {v}")


# ---------------------------------------------------------------------- #
# 3. Priority Queue
# ---------------------------------------------------------------------- #
def bench_pq(incidentes) -> None:
    sep("PARTE 3 - PRIORITY QUEUE (Heap)")
    pq = PriorityQueue()
    _, t_push = _timeit(lambda: [pq.push(i, i.score(AHORA)) for i in incidentes])
    print(f"\nInsercion (push) de {len(incidentes)} incidentes: {t_push * 1000:.3f} ms")

    print("\nTop-5 incidentes mas criticos:")
    for inc in pq.top_k(5):
        print(f"  {inc.id}  zona={inc.zona:>4}  prioridad={inc.prioridad.name:8s}"
              f"  score={inc.score(AHORA):8.2f}")

    # Extraccion completa ordenada (debe salir de mayor a menor score).
    scores = []
    while not pq.is_empty():
        scores.append(pq.pop().score(AHORA))
    assert all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)), \
        "El heap no respeta el orden de prioridad"
    print("\n  Orden de extraccion verificado (mayor prioridad primero). OK")


# ---------------------------------------------------------------------- #
# 4. Pathfinding: BFS vs UCS vs A*
# ---------------------------------------------------------------------- #
def bench_pathfinding(graph, centros) -> None:
    sep("PARTE 6 - BUSQUEDA DE RUTAS: BFS vs UCS/Dijkstra vs A*")
    rng = random.Random(99)
    nodos = graph.nodes()
    pares = [(rng.choice(nodos), rng.choice(nodos)) for _ in range(200)]

    for nombre, algo in [("BFS", bfs), ("UCS/Dijkstra", ucs), ("A*", a_star)]:
        t0 = time.perf_counter()
        visitados = 0
        encontrados = 0
        for s, g in pares:
            r = algo(graph, s, g)
            visitados += r.num_visited
            encontrados += 1 if r.found else 0
        dt = time.perf_counter() - t0
        print(f"\n{nombre}")
        print(f"  tiempo total ({len(pares)} consultas): {dt * 1000:8.3f} ms")
        print(f"  nodos expandidos (promedio)        : {visitados / len(pares):8.1f}")
        print(f"  rutas encontradas                  : {encontrados}/{len(pares)}")

    # Comparacion de costo: UCS y A* deben coincidir en costo optimo.
    s, g = centros[0].ubicacion, nodos[-1]
    ru, ra = ucs(graph, s, g), a_star(graph, s, g)
    if ru.found and ra.found:
        print(f"\nVerificacion optimalidad {s}->{g}:")
        print(f"  Costo UCS = {ru.cost:.2f} | Costo A* = {ra.cost:.2f}"
              f"  ({'coinciden' if abs(ru.cost - ra.cost) < 1e-6 else 'DIFIEREN'})")
        print(f"  A* expandio {ra.num_visited} nodos vs {ru.num_visited} de UCS")


# ---------------------------------------------------------------------- #
# 5. Ranking de zonas
# ---------------------------------------------------------------------- #
def bench_zonas(incidentes) -> None:
    sep("ANALISIS - Zonas con mas incidentes")
    ranking = contar_por_zona(incidentes)
    print("\nTop-10 zonas por frecuencia:")
    for zona, n in ranking[:10]:
        print(f"  zona {zona:>4}: {n} incidentes")


def main() -> None:
    print("Cargando dataset...")
    incidentes = load_incidents()
    graph = load_network()
    centros = load_centers()
    print(f"  incidentes: {len(incidentes)} | {graph} | centros: {len(centros)}")

    bench_hash(incidentes)
    bench_pq(incidentes)
    bench_sorting(incidentes)
    bench_zonas(incidentes)
    bench_pathfinding(graph, centros)

    sep("ANALISIS EXPERIMENTAL COMPLETADO")


if __name__ == "__main__":
    main()