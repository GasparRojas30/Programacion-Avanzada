import heapq
from typing import Any, Dict, Optional, List, Callable
from .base import SearchAlgorithm


class AStar(SearchAlgorithm):
    
    def search(self, graph: Any, start: Any, goal: Any, heuristic: Optional[Callable] = None) -> Dict:
        
        self.visited = []
        self.path = []
        self.cost = 0
        self.nodes_expanded = 0
        self.frontier_max_size = 0
        
        if heuristic is None:
            raise ValueError("A* requires a heuristic function")
        
        if start == goal:
            return {
                'path': [start],
                'visited': [start],
                'cost': 0,
                'success': True,
                'nodes_expanded': 0
            }
        
        counter = 0
        h_start = heuristic(start, goal)
        heap = [(h_start, counter, start)]
        counter += 1
        
        visited_set = set()
        parent = {start: None}
        g_score = {start: 0}
        f_score = {start: h_start}
        
        while heap:
            self.frontier_max_size = max(self.frontier_max_size, len(heap))
            current_f, _, current = heapq.heappop(heap)
            
            if current in visited_set:
                continue
            
            visited_set.add(current)
            self.visited.append(current)
            self.nodes_expanded += 1
            
            if current == goal:
                self.path = self._extract_path(parent, start, goal)
                self.cost = g_score[current]
                return {
                    'path': self.path,
                    'visited': self.visited,
                    'cost': self.cost,
                    'success': True,
                    'nodes_expanded': self.nodes_expanded
                }
            
            neighbors = graph.get_neighbors_with_cost(current)
            
            for neighbor, edge_cost in neighbors:
                if neighbor not in visited_set:
                    tentative_g = g_score[current] + edge_cost
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        parent[neighbor] = current
                        g_score[neighbor] = tentative_g
                        h_neighbor = heuristic(neighbor, goal)
                        f_score[neighbor] = tentative_g + h_neighbor
                        heapq.heappush(heap, (f_score[neighbor], counter, neighbor))
                        counter += 1
        
        return {
            'path': [],
            'visited': self.visited,
            'cost': float('inf'),
            'success': False,
            'nodes_expanded': self.nodes_expanded
        }
