from __future__ import annotations

import csv
import json
import math
import os
import random
from datetime import datetime, timedelta

try:
    from ..models.incident import Incident, Priority, IncidentType, IncidentStatus
except ImportError:  # ejecucion directa
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models.incident import Incident, Priority, IncidentType, IncidentStatus  # type: ignore


DATA_DIR = os.path.dirname(os.path.abspath(__file__))

N_NODES = 50
N_EXTRA_EDGES_TARGET = 110   # >= 100 aristas exigidas
N_INCIDENTS = 500
N_CENTERS = 4


def generar_grafo(n_nodes: int = N_NODES, n_edges: int = N_EXTRA_EDGES_TARGET,
                  seed: int = 42):
    """
    Genera nodos con coordenadas y aristas ponderadas.
    """
    rng = random.Random(seed)
    nodes = [(f"N{i}", round(rng.uniform(0, 100), 2), round(rng.uniform(0, 100), 2))
             for i in range(n_nodes)]
    coord = {nid: (x, y) for nid, x, y in nodes}

    def peso(u: str, v: str) -> float:
        (x1, y1), (x2, y2) = coord[u], coord[v]
        d = math.hypot(x1 - x2, y1 - y2)
        return round(d * rng.uniform(1.0, 1.4), 1)

    edges: list[tuple[str, str, float]] = []
    existentes: set[frozenset[str]] = set()

    for i in range(1, n_nodes):
        j = rng.randint(0, i - 1)
        u, v = f"N{i}", f"N{j}"
        edges.append((u, v, peso(u, v)))
        existentes.add(frozenset((u, v)))

    while len(edges) < n_edges:
        a, b = rng.sample(range(n_nodes), 2)
        u, v = f"N{a}", f"N{b}"
        if frozenset((u, v)) in existentes:
            continue
        edges.append((u, v, peso(u, v)))
        existentes.add(frozenset((u, v)))

    return nodes, edges


def generar_centros(nodes, n: int = N_CENTERS, seed: int = 7):
    """Ubica n centros de emergencia en nodos distintos del grafo."""
    rng = random.Random(seed)
    ids = [nid for nid, _, _ in nodes]
    elegidos = rng.sample(ids, min(n, len(ids)))
    nombres = ["Centro Norte", "Centro Sur", "Centro Este", "Centro Oeste",
               "Centro Central", "Centro Litoral"]
    return [(f"C-{i}", nombres[i % len(nombres)], nodo)
            for i, nodo in enumerate(elegidos)]

def generar_incidentes(nodes, n: int = N_INCIDENTS, seed: int = 123):
    """
    Genera n incidentes distribuidos en las zonas (nodos) del grafo.
    Los timestamps se reparten en las ultimas 24 horas respecto a `ahora`.
    """
    rng = random.Random(seed)
    zonas = [nid for nid, _, _ in nodes]
    ahora = datetime(2026, 7, 11, 12, 0, 0)
    incidentes: list[Incident] = []
    for i in range(n):
        prioridad = rng.choices(
            [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL],
            weights=[4, 3, 2, 1],
        )[0]
        tipo = rng.choice(list(IncidentType))
        minutos_atras = rng.randint(1, 24 * 60)
        ts = ahora - timedelta(minutes=minutos_atras)
        severidad = rng.randint(1, 5)
        incidentes.append(Incident(
            id=f"I-{i:04d}",
            zona=rng.choice(zonas),
            prioridad=prioridad,
            tipo=tipo,
            timestamp=ts,
            estado=IncidentStatus.REPORTED,
            severidad=severidad,
        ))
    return incidentes

def escribir_datos(data_dir: str = DATA_DIR, seed: int = 42) -> None:
    nodes, edges = generar_grafo(seed=seed)
    centros = generar_centros(nodes)
    incidentes = generar_incidentes(nodes)

    # nodos.csv
    with open(os.path.join(data_dir, "nodos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "x", "y"])
        w.writerows(nodes)

    # red_vial.csv
    with open(os.path.join(data_dir, "red_vial.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["origen", "destino", "peso"])
        w.writerows(edges)

    # red_vial.json (formato alternativo de carga)
    with open(os.path.join(data_dir, "red_vial.json"), "w", encoding="utf-8") as f:
        json.dump({
            "nodes": [{"id": n, "x": x, "y": y} for n, x, y in nodes],
            "edges": [{"origen": u, "destino": v, "peso": w} for u, v, w in edges],
        }, f, indent=2)

    # centros.csv
    with open(os.path.join(data_dir, "centros.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "nombre", "ubicacion"])
        w.writerows(centros)

    # incidentes.csv
    with open(os.path.join(data_dir, "incidentes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "zona", "prioridad", "tipo", "timestamp", "severidad", "estado"])
        for inc in incidentes:
            w.writerow([
                inc.id, inc.zona, int(inc.prioridad), int(inc.tipo),
                inc.timestamp.isoformat(), inc.severidad, int(inc.estado),
            ])

    print("Datos generados en:", data_dir)
    print(f"  nodos.csv       : {len(nodes)} nodos")
    print(f"  red_vial.csv    : {len(edges)} aristas")
    print(f"  centros.csv     : {len(centros)} centros")
    print(f"  incidentes.csv  : {len(incidentes)} incidentes")


if __name__ == "__main__":
    escribir_datos()