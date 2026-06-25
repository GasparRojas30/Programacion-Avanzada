import csv
from typing import List, Dict, Tuple, Optional


class Graph:
    
    def __init__(self):
        self.graph = {}
        self.costs = {}
    
    def add_node(self, node: str):
        """Add a node to the graph."""
        if node not in self.graph:
            self.graph[node] = []
    
    def add_edge(self, node1: str, node2: str, cost: float = 1.0, directed: bool = False):
    
        self.add_node(node1)
        self.add_node(node2)
        
        self.graph[node1].append(node2)
        self.costs[(node1, node2)] = cost
        
        if not directed:
            self.graph[node2].append(node1)
            self.costs[(node2, node1)] = cost
    
    def get_neighbors(self, node: str) -> List[str]:
        return self.graph.get(node, [])
    
    def get_neighbors_with_cost(self, node: str) -> List[Tuple[str, float]]:
        neighbors = []
        for neighbor in self.graph.get(node, []):
            cost = self.costs.get((node, neighbor), 1.0)
            neighbors.append((neighbor, cost))
        return neighbors
    
    def get_nodes(self) -> List[str]:
        """Get all nodes in the graph."""
        return list(self.graph.keys())
    
    def from_csv(self, filename: str, directed: bool = False):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                source = row['source'].strip()
                target = row['target'].strip()
                cost = float(row.get('cost', 1.0))
                self.add_edge(source, target, cost, directed=directed)
    
    def to_csv(self, filename: str):
        edges_set = set()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['source', 'target', 'cost'])
            writer.writeheader()
            
            for node1 in self.graph:
                for node2 in self.graph[node1]:
                    edge = tuple(sorted([node1, node2]))
                    if edge not in edges_set:
                        cost = self.costs.get((node1, node2), 1.0)
                        writer.writerow({
                            'source': node1,
                            'target': node2,
                            'cost': cost
                        })
                        edges_set.add(edge)
    
    @staticmethod
    def create_example_graph() -> 'Graph':
        g = Graph()
        edges = [
            ('A', 'B', 4),
            ('A', 'C', 2),
            ('B', 'C', 1),
            ('B', 'D', 5),
            ('C', 'D', 8),
            ('C', 'E', 10),
            ('D', 'E', 2),
            ('D', 'F', 6),
            ('E', 'F', 3)
        ]
        
        for n1, n2, cost in edges:
            g.add_edge(n1, n2, cost, directed=False)
        
        return g
