from typing import Any, Dict, Optional, List
from .base import SearchAlgorithm


class DFS(SearchAlgorithm):
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
        
        stack = [start]
        visited_set = {start}
        parent = {start: None}
        
        while stack:
            self.frontier_max_size = max(self.frontier_max_size, len(stack))
            current = stack.pop()
            self.visited.append(current)
            self.nodes_expanded += 1
            
            if current == goal:
                self.path = self._extract_path(parent, start, goal)
                return {
                    'path': self.path,
                    'visited': self.visited,
                    'cost': len(self.path) - 1,  
                    'success': True,
                    'nodes_expanded': self.nodes_expanded
                }
            
            neighbors = graph.get_neighbors(current)
            
            for neighbor in reversed(neighbors):
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    stack.append(neighbor)
                    parent[neighbor] = current
        
        return {
            'path': [],
            'visited': self.visited,
            'cost': float('inf'),
            'success': False,
            'nodes_expanded': self.nodes_expanded
        }
