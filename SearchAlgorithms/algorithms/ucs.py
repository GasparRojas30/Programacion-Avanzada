import heapq
from typing import Any, Dict, Optional, List
from .base import SearchAlgorithm


class UCS(SearchAlgorithm):

    def search(self, graph: Any, start: Any, goal: Any, heuristic: Optional[callable] = None) -> Dict:
    
        self.visited = []
        self.path = []
        self.cost = 0
        self.nodes_expanded = 0
        self.frontier_max_size = 0
        
        if start == goal:
            return {
                'path': [start],
                'visited': [start],
                'cost': 0,
                'success': True,
                'nodes_expanded': 0
            }
        
        counter = 0
        heap = [(0, counter, start)]
        counter += 1
        
        visited_set = set()
        parent = {start: None}
        cost_so_far = {start: 0}
        
        while heap:
            self.frontier_max_size = max(self.frontier_max_size, len(heap))
            current_cost, _, current = heapq.heappop(heap)
            
            if current in visited_set:
                continue
            
            visited_set.add(current)
            self.visited.append(current)
            self.nodes_expanded += 1
            
            if current == goal:
                self.path = self._extract_path(parent, start, goal)
                self.cost = current_cost
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
                    new_cost = cost_so_far[current] + edge_cost
                    
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        parent[neighbor] = current
                        heapq.heappush(heap, (new_cost, counter, neighbor))
                        counter += 1
        
        return {
            'path': [],
            'visited': self.visited,
            'cost': float('inf'),
            'success': False,
            'nodes_expanded': self.nodes_expanded
        }
