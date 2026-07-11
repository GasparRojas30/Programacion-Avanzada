from __future__ import annotations

"""
Parte 7 - Escenario integrado del Sistema de Gestion de Emergencias.

Flujo:
  1. Leer incidentes.csv (y la red vial + centros).
  2. Insertar los incidentes en la Tabla Hash y en la Priority Queue.
  3. Extraer el incidente mas urgente.
  4. Buscar la ruta optima desde el centro de emergencia mas cercano.
  5. Mostrar: incidente asignado, prioridad, ruta sugerida, costo total y
     tiempo estimado.

Uso:
  python -m Emergency_System.main            # ejecuta el escenario integrado
  python -m Emergency_System.main --reportes # ademas imprime reportes
"""

import os
import sys
from datetime import datetime

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Emergency_System.data.loaders import load_incidents, load_network, load_centers
from Emergency_System.data import generator
from Emergency_System.structures.hash_table import HashTable
from Emergency_System.structures.priority_queue import PriorityQueue
from Emergency_System.structures.sorting import merge_sort, contar_por_zona
from Emergency_System.algorithms.pathfinding import ucs, a_star, bfs
from Emergency_System.models.incident import IncidentStatus

AHORA = datetime(2026, 7, 11, 12, 0, 0)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def _asegurar_datos() -> None:
    incidentes_csv = os.path.join(DATA_DIR, "incidentes.csv")
    if not os.path.exists(incidentes_csv) or os.path.getsize(incidentes_csv) == 0:
        print("Dataset no encontrado. Generandolo...\n")
        generator.escribir_datos(DATA_DIR)
        print()


def centro_mas_cercano(graph, centros, zona: str):
    mejor_centro = None
    mejor_ruta = None
    for c in centros:
        r = ucs(graph, c.ubicacion, zona)
        if r.found and (mejor_ruta is None or r.cost < mejor_ruta.cost):
            mejor_centro, mejor_ruta = c, r
    return mejor_centro, mejor_ruta


def escenario_integrado() -> None:
    print("#" * 64)
    print("#  SISTEMA DE GESTION DE EMERGENCIAS - ESCENARIO INTEGRADO")
    print("#" * 64)

    print("\n[Paso 1] Leyendo datos...")
    incidentes = load_incidents()
    graph = load_network()
    centros = load_centers()
    print(f"  Incidentes  : {len(incidentes)}")
    print(f"  Red vial    : {graph}")
    print(f"  Centros     : {len(centros)}")

    print("\n[Paso 2] Insertando en Tabla Hash y Priority Queue...")
    ht = HashTable()
    pq = PriorityQueue()
    for inc in incidentes:
        ht.insert(inc.id, inc)
        pq.push(inc, inc.score(AHORA))
    st = ht.stats()
    print(f"  Hash -> factor_carga={st['factor_carga']} colisiones={st['colisiones']} "
          f"buckets_util={st['buckets_utilizados']} max_bucket={st['max_tamano_bucket']}")
    print(f"  PQ   -> {len(pq)} incidentes encolados")

    print("\n[Paso 3] Extrayendo el incidente mas urgente...")
    urgente = pq.pop()
    print(f"  Incidente mas urgente: {urgente.id} (score={urgente.score(AHORA):.2f})")

    print("\n[Paso 4] Calculando ruta optima desde el centro mas cercano...")
    centro, ruta = centro_mas_cercano(graph, centros, urgente.zona)

    print("\n[Paso 5] RESULTADO DEL DESPACHO")
    print("-" * 64)
    print(f"  Incidente asignado : {urgente.id}")
    print(f"  Zona (nodo)        : {urgente.zona}")
    print(f"  Tipo               : {urgente.tipo.name}")
    print(f"  Prioridad          : {urgente.prioridad.name} (severidad {urgente.severidad})")
    print(f"  Reportado          : {urgente.timestamp.isoformat()}")
    if centro and ruta:
        print(f"  Centro asignado    : {centro.id} - {centro.nombre} (nodo {centro.ubicacion})")
        print(f"  Ruta sugerida      : {' -> '.join(ruta.path)}")
        print(f"  Nodos visitados    : {ruta.num_visited}")
        print(f"  Costo total        : {ruta.cost:.2f}")
        print(f"  Tiempo estimado    : {ruta.cost:.1f} minutos")
        ht.update_state(urgente.id, IncidentStatus.ASSIGNED)
        print(f"  Estado actualizado : {ht.search(urgente.id).estado.name}")

        ra = a_star(graph, centro.ubicacion, urgente.zona)
        print(f"  [A* verificacion]  : costo={ra.cost:.2f}, "
              f"nodos={ra.num_visited} (UCS uso {ruta.num_visited})")
    else:
        print("  No se encontro ruta hacia el incidente.")
    print("-" * 64)


def reportes() -> None:
    print("\n" + "#" * 64)
    print("#  REPORTES Y ESTADISTICAS")
    print("#" * 64)
    incidentes = load_incidents()

    print("\n>> Top-10 incidentes MAS CRITICOS (por score):")
    criticos = merge_sort(incidentes, key=lambda i: i.score(AHORA), reverse=True)
    for inc in criticos[:10]:
        print(f"   {inc.id}  {inc.prioridad.name:8s}  zona={inc.zona:>4}  "
              f"score={inc.score(AHORA):8.2f}")

    print("\n>> Top-10 incidentes MAS ANTIGUOS:")
    antiguos = merge_sort(incidentes, key=lambda i: i.timestamp)
    for inc in antiguos[:10]:
        print(f"   {inc.id}  {inc.timestamp.isoformat()}  zona={inc.zona}")

    print("\n>> Top-10 ZONAS con mas incidentes:")
    for zona, n in contar_por_zona(incidentes)[:10]:
        print(f"   zona {zona:>4}: {n} incidentes")


def main() -> None:
    _asegurar_datos()
    escenario_integrado()
    if "--reportes" in sys.argv or "-r" in sys.argv:
        reportes()


if __name__ == "__main__":
    main()