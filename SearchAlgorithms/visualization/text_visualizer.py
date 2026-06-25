from typing import List, Dict, Any


class TextVisualizer:
    
    @staticmethod
    def display_results(results: Dict, scenario_type: str = "Graph", 
                       algorithm_name: str = "Unknown", start: Any = None, 
                       goal: Any = None):
        """Display search results in text format."""
        print("\n" + "="*70)
        print(f"SEARCH RESULTS - {scenario_type.upper()} | {algorithm_name.upper()}")
        print("="*70)
        
        print(f"\nStart: {start}")
        print(f"Goal: {goal}")
        
        print(f"\n{'─'*70}")
        print("STATISTICS:")
        print(f"{'─'*70}")
        print(f"Success: {'✓ YES' if results['success'] else '✗ NO'}")
        print(f"Cost: {results['cost'] if results['cost'] != float('inf') else 'N/A'}")
        print(f"Nodes Expanded: {results['nodes_expanded']}")
        print(f"Path Length: {len(results['path'])}")
        print(f"Visited Nodes: {len(results['visited'])}")
        
        print(f"\n{'─'*70}")
        print("VISITED ORDER:")
        print(f"{'─'*70}")
        if results['visited']:
            visited_str = " → ".join(str(n) for n in results['visited'][:20])
            if len(results['visited']) > 20:
                visited_str += f" ... and {len(results['visited']) - 20} more"
            print(visited_str)
        else:
            print("None")
        
        print(f"\n{'─'*70}")
        print("FINAL PATH:")
        print(f"{'─'*70}")
        if results['path']:
            path_str = " → ".join(str(n) for n in results['path'])
            print(path_str)
        else:
            print("No path found!")
        
        print(f"\n{'='*70}\n")
    
    @staticmethod
    def display_visited_heatmap(visited: List[Any], grid_size: int = 10):
        """Display visited cells as a heatmap (text-based)."""
        print("\nVisited Cells Heatmap (Order by visit):")
        print("─" * (grid_size * 2 + 1))
        
        visited_dict = {node: idx for idx, node in enumerate(visited)}
        
        for i in range(grid_size):
            row = ""
            for j in range(grid_size):
                if (i, j) in visited_dict:
                    intensity = visited_dict[(i, j)] % 10
                    row += f"{intensity} "
                else:
                    row += ". "
            print(row)
        
        print("─" * (grid_size * 2 + 1))
