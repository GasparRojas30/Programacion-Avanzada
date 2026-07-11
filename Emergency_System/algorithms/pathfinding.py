from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Optional

from ..models.road_network import RoadNetwork
from ..structures.priority_queue import PriorityQueue


@dataclass
class SearchResult:

    found: bool
    path: list[str] = field(default_factory=list)
    cost: float = 0.0
    visited: list[str] = field(default_factory=list)
    algorithm: str = ""

    @property
    def num_visited(self) -> int:
        return len(self.visited)

    def describe(self) -> str:
        if not self.found:
            return f"[{self.algorithm}] No existe ruta."
        ruta = " -> ".join(self.path)
        return (
            f"[{self.algorithm}] Ruta: {ruta}\n"
            f"    Nodos visitados : {self.num_visited}\n"
            f"    Distancia/Costo : {self.cost:.2f}"
        )


def _reconstruct(came_from: dict[str, Optional[str]], goal: str) -> list[str]:
    path: list[str] = []
    cur: Optional[str] = goal
    while cur is not None:
        path.append(cur)
        cur = came_from.get(cur)
    path.reverse()
    return path


def _path_cost(graph: RoadNetwork, path: list[str]) -> float:
    total = 0.0
    for u, v in zip(path, path[1:]):
        w = graph.weight(u, v)
        total += w if w is not None else 0.0
    return total

def bfs(graph: RoadNetwork, start: str, goal: str) -> SearchResult:
    """
    Busqueda en anchura: encuentra la ruta con MENOR NUMERO DE ARISTAS
    (ignora los pesos). Util como baseline.

    Complejidad: O(V + E).
    pre: start y goal existen en el grafo.
    post: si found, path es un camino start->goal con minimo numero de saltos.
    """
    if start == goal:
        return SearchResult(True, [start], 0.0, [start], "BFS")

    frontier: deque[str] = deque([start])
    came_from: dict[str, Optional[str]] = {start: None}
    visited: list[str] = []

    while frontier:
        node = frontier.popleft()
        visited.append(node)
        if node == goal:
            path = _reconstruct(came_from, goal)
            return SearchResult(True, path, _path_cost(graph, path), visited, "BFS")
        for neighbor, _w in graph.neighbors(node):
            if neighbor not in came_from:
                came_from[neighbor] = node
                frontier.append(neighbor)

    return SearchResult(False, [], 0.0, visited, "BFS")

def ucs(graph: RoadNetwork, start: str, goal: str) -> SearchResult:
    """
    Uniform Cost Search (equivalente a Dijkstra de origen unico):
    encuentra la ruta de MENOR COSTO acumulado (suma de pesos).

    Reutiliza la PriorityQueue propia como cola de MINIMOS usando
    prioridad = -costo (la cola es un max-heap).

    Complejidad: O((V + E) log V).
    pre: todos los pesos >= 0.
    post: si found, path es el camino de costo minimo start->goal.
    """
    dist: dict[str, float] = {start: 0.0}
    came_from: dict[str, Optional[str]] = {start: None}
    settled: set[str] = set()
    visited: list[str] = []

    pq = PriorityQueue()
    pq.push(start, priority=0.0, key=start)

    while not pq.is_empty():
        node = pq.pop()
        if node in settled:
            continue
        settled.add(node)
        visited.append(node)

        if node == goal:
            path = _reconstruct(came_from, goal)
            return SearchResult(True, path, dist[node], visited, "UCS/Dijkstra")

        for neighbor, w in graph.neighbors(node):
            if neighbor in settled:
                continue
            new_cost = dist[node] + w
            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                came_from[neighbor] = node
                pq.push(neighbor, priority=-new_cost, key=neighbor)

    return SearchResult(False, [], 0.0, visited, "UCS/Dijkstra")


def a_star(graph: RoadNetwork, start: str, goal: str) -> SearchResult:
    """
    A* con heuristica de distancia euclidiana (admisible mientras el peso
    de cada arista sea >= la distancia euclidiana entre sus extremos).

    f(n) = g(n) + h(n)
        g(n) = costo real acumulado desde start.
        h(n) = distancia euclidiana estimada hasta goal.

    Complejidad: O((V + E) log V) en el peor caso; en la practica expande
    muchos menos nodos que UCS gracias a la heuristica.
    """
    g: dict[str, float] = {start: 0.0}
    came_from: dict[str, Optional[str]] = {start: None}
    settled: set[str] = set()
    visited: list[str] = []

    pq = PriorityQueue()
    pq.push(start, priority=-graph.heuristic(start, goal), key=start)

    while not pq.is_empty():
        node = pq.pop()
        if node in settled:
            continue
        settled.add(node)
        visited.append(node)

        if node == goal:
            path = _reconstruct(came_from, goal)
            return SearchResult(True, path, g[node], visited, "A*")

        for neighbor, w in graph.neighbors(node):
            if neighbor in settled:
                continue
            tentative = g[node] + w
            if neighbor not in g or tentative < g[neighbor]:
                g[neighbor] = tentative
                came_from[neighbor] = node
                f = tentative + graph.heuristic(neighbor, goal)
                pq.push(neighbor, priority=-f, key=neighbor)

    return SearchResult(False, [], 0.0, visited, "A*")