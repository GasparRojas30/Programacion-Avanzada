from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass, field


@dataclass
class Node:
    """Nodo de la red vial: una interseccion o localidad.

    x, y son coordenadas planas (metros/unidades arbitrarias) usadas por
    la heuristica de A*.
    """

    id: str
    x: float = 0.0
    y: float = 0.0

class RoadNetwork:

    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._adj: dict[str, list[tuple[str, float]]] = {}

    def add_node(self, node_id: str, x: float = 0.0, y: float = 0.0) -> None:
        """pre: node_id no vacio. post: el nodo existe en el grafo."""
        if node_id not in self._nodes:
            self._nodes[node_id] = Node(node_id, x, y)
            self._adj[node_id] = []
        else:
            n = self._nodes[node_id]
            if (n.x, n.y) == (0.0, 0.0) and (x, y) != (0.0, 0.0):
                n.x, n.y = x, y

    def add_edge(self, u: str, v: str, weight: float, dirigido: bool = False) -> None:
        if weight < 0:
            raise ValueError("Los pesos de la red vial no pueden ser negativos.")
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append((v, float(weight)))
        if not dirigido:
            self._adj[v].append((u, float(weight)))

    def neighbors(self, u: str) -> list[tuple[str, float]]:
        return self._adj.get(u, [])

    def weight(self, u: str, v: str) -> float | None:
        for w_node, w in self._adj.get(u, []):
            if w_node == v:
                return w
        return None

    def has_node(self, u: str) -> bool:
        return u in self._nodes

    def nodes(self) -> list[str]:
        return list(self._nodes.keys())

    def node(self, u: str) -> Node | None:
        return self._nodes.get(u)

    def edges(self) -> list[tuple[str, str, float]]:
        out: list[tuple[str, str, float]] = []
        for u, lst in self._adj.items():
            for v, w in lst:
                out.append((u, v, w))
        return out

    def num_nodes(self) -> int:
        return len(self._nodes)

    def num_edges(self) -> int:
        return sum(len(lst) for lst in self._adj.values())

    def heuristic(self, u: str, v: str) -> float:
        a = self._nodes.get(u)
        b = self._nodes.get(v)
        if a is None or b is None:
            return 0.0
        return math.hypot(a.x - b.x, a.y - b.y)

    def load_csv(self, edges_path: str, nodes_path: str | None = None) -> None:
        if nodes_path and os.path.exists(nodes_path):
            with open(nodes_path, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    self.add_node(row["id"], float(row["x"]), float(row["y"]))

        with open(edges_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                dirigido = str(row.get("dirigido", "0")).strip() in ("1", "true", "True")
                self.add_edge(row["origen"], row["destino"], float(row["peso"]), dirigido)

    def load_json(self, path: str) -> None:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for n in data.get("nodes", []):
            self.add_node(n["id"], float(n.get("x", 0)), float(n.get("y", 0)))
        for e in data.get("edges", []):
            self.add_edge(
                e["origen"], e["destino"], float(e["peso"]),
                bool(e.get("dirigido", False)),
            )

    def __repr__(self) -> str:
        return f"RoadNetwork(nodos={self.num_nodes()}, aristas={self.num_edges()})"