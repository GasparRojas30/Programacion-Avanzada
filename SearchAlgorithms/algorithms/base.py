from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any


class SearchAlgorithm(ABC):    
    def __init__(self):
        self.visited = []
        self.path = []
        self.cost = 0
        self.nodes_expanded = 0
        self.frontier_max_size = 0
    
    @abstractmethod
    def search(self, graph: Any, start: Any, goal: Any, heuristic: Optional[callable] = None) -> Dict:
        pass
    
    def _extract_path(self, parent: Dict, start: Any, goal: Any) -> List:
        path = []
        current = goal
        
        while current is not None:
            path.append(current)
            current = parent.get(current)
        
        path.reverse()
        return path
