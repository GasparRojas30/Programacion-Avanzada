

import os
import sys
from typing import Tuple, Optional

from algorithms import BFS, DFS, UCS, AStar
from scenarios import Graph, Maze
from visualization import TextVisualizer, GraphVisualizer, MazeVisualizer


class SearchAlgorithmApp:    
    def __init__(self):
        self.algorithms = {
            '1': ('BFS', BFS()),
            '2': ('DFS', DFS()),
            '3': ('UCS', UCS()),
            '4': ('A*', AStar())
        }
        self.current_scenario = None
        self.current_type = None
    
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        print("\n" + "="*70)
        print("   SEARCH ALGORITHMS VISUALIZATION SYSTEM".center(70))
        print("="*70)
        print("\n" + "BFS | DFS | UCS | A*".center(70))
        print("─"*70)
    
    def select_scenario(self) -> Tuple[str, object]:
        self.clear_screen()
        self.print_header()
        
        print("\n1. GRAPH SCENARIO")
        print("   Search in graph/tree structures")
        print("\n2. MAZE SCENARIO")
        print("   Search in maze/grid environments")
        
        choice = input("\nSelect scenario (1-2): ").strip()
        
        if choice == '1':
            return 'graph', self.setup_graph()
        elif choice == '2':
            return 'maze', self.setup_maze()
        else:
            print("Invalid choice!")
            return self.select_scenario()
    
    def setup_graph(self) -> Graph:
        print("\n" + "─"*70)
        print("GRAPH SETUP")
        print("─"*70)
        
        print("\n1. Load from CSV file")
        print("2. Use example graph")
        print("3. Create custom graph")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            filename = input("Enter CSV filename (relative to SearchAlgorithms): ").strip()
            filepath = os.path.join(os.path.dirname(__file__), '..', filename)
            try:
                g = Graph()
                g.from_csv(filepath)
                print(f" Loaded graph with {len(g.get_nodes())} nodes")
                return g
            except FileNotFoundError:
                print(f" File not found: {filepath}")
                return self.setup_graph()
        
        elif choice == '2':
            g = Graph.create_example_graph()
            print(" Loaded example graph")
            print(f"Nodes: {', '.join(g.get_nodes())}")
            return g
        
        elif choice == '3':
            g = Graph()
            print("\nEnter edges (format: node1 node2 cost)")
            print("Type 'done' to finish")
            while True:
                line = input(">> ").strip()
                if line.lower() == 'done':
                    break
                try:
                    parts = line.split()
                    if len(parts) >= 2:
                        node1, node2 = parts[0], parts[1]
                        cost = float(parts[2]) if len(parts) > 2 else 1.0
                        g.add_edge(node1, node2, cost)
                except:
                    print("Invalid format! Use: node1 node2 [cost]")
            return g
        
        return Graph.create_example_graph()
    
    def setup_maze(self) -> Maze:
        print("\n" + "─"*70)
        print("MAZE SETUP")
        print("─"*70)
        
        print("\n1. Load from file")
        print("2. Use example maze")
        print("3. Create random maze")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            filename = input("Enter maze filename (relative to SearchAlgorithms): ").strip()
            filepath = os.path.join(os.path.dirname(__file__), '..', filename)
            try:
                m = Maze([[]])
                m.load_from_file(filepath)
                print(f" Loaded maze ({m.rows}×{m.cols})")
                return m
            except FileNotFoundError:
                print(f" File not found: {filepath}")
                return self.setup_maze()
        
        elif choice == '2':
            m = Maze.create_example_maze()
            print(f" Loaded example maze ({m.rows}×{m.cols})")
            return m
        
        elif choice == '3':
            try:
                rows = int(input("Maze height: "))
                cols = int(input("Maze width: "))
                barrier_prob = float(input("Barrier probability (0-1): "))
                
                import random
                grid = []
                for i in range(rows):
                    row = []
                    for j in range(cols):
                        if (i == 0 or i == rows-1) or (j == 0 or j == cols-1):
                            row.append(random.choice([0, 1]) if random.random() < barrier_prob else 0)
                        else:
                            row.append(1 if random.random() < barrier_prob else 0)
                    grid.append(row)
                
                m = Maze(grid)
                print(f"✓ Generated random maze ({m.rows}×{m.cols})")
                return m
            except:
                return self.setup_maze()
        
        return Maze.create_example_maze()
    
    def select_algorithm(self) -> Tuple[str, object]:
        """Let user select search algorithm."""
        print("\n" + "─"*70)
        print("ALGORITHM SELECTION")
        print("─"*70)
        
        print("\n1. BFS (Breadth-First Search)")
        print("   - Explores by levels")
        print("   - Optimal for unweighted graphs")
        
        print("\n2. DFS (Depth-First Search)")
        print("   - Explores in depth")
        print("   - Memory efficient")
        
        print("\n3. UCS (Uniform Cost Search)")
        print("   - Expands by cost")
        print("   - Optimal for weighted graphs")
        
        print("\n4. A* (A-Star)")
        print("   - Uses heuristic + cost")
        print("   - Most efficient with good heuristic")
        
        choice = input("\nSelect algorithm (1-4): ").strip()
        
        if choice in self.algorithms:
            return self.algorithms[choice]
        else:
            print("Invalid choice!")
            return self.select_algorithm()
    
    def get_start_goal_graph(self) -> Tuple[str, str]:
        nodes = self.current_scenario.get_nodes()
        print(f"\nAvailable nodes: {', '.join(nodes)}")
        
        start = input("Start node: ").strip()
        goal = input("Goal node: ").strip()
        
        if start not in nodes:
            print(f" Node '{start}' not in graph!")
            return self.get_start_goal_graph()
        if goal not in nodes:
            print(f" Node '{goal}' not in graph!")
            return self.get_start_goal_graph()
        
        return start, goal
    
    def get_start_goal_maze(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        maze = self.current_scenario
        
        print(f"\nMaze size: {maze.rows}×{maze.cols}")
        
        try:
            start_row = int(input("Start row (0-{}): ".format(maze.rows-1)))
            start_col = int(input("Start col (0-{}): ".format(maze.cols-1)))
            goal_row = int(input("Goal row (0-{}): ".format(maze.rows-1)))
            goal_col = int(input("Goal col (0-{}): ".format(maze.cols-1)))
            
            start = (start_row, start_col)
            goal = (goal_row, goal_col)
            
            if not maze.is_valid_position(start[0], start[1]):
                print(" Start position is invalid (barrier or out of bounds)!")
                return self.get_start_goal_maze()
            
            if not maze.is_valid_position(goal[0], goal[1]):
                print(" Goal position is invalid (barrier or out of bounds)!")
                return self.get_start_goal_maze()
            
            return start, goal
        except:
            print(" Invalid input!")
            return self.get_start_goal_maze()
    
    def run_search(self, algorithm_name: str, algorithm: object, 
                   start: any, goal: any) -> dict:
        print("\n" + "─"*70)
        print("EXECUTING SEARCH...")
        print("─"*70)
        
        if self.current_type == 'graph':
            if algorithm_name == 'A*':
                def heuristic(n1, n2):
                    return 0  
                
                results = algorithm.search(self.current_scenario, start, goal, heuristic)
            else:
                results = algorithm.search(self.current_scenario, start, goal)
        
        else:
            if algorithm_name == 'A*':
                heuristic = self.current_scenario.manhattan_distance
                results = algorithm.search(self.current_scenario, start, goal, heuristic)
            else:
                results = algorithm.search(self.current_scenario, start, goal)
        
        return results
    
    def visualize_results(self, results: dict, algorithm_name: str, 
                         start: any, goal: any):
        print("\n" + "─"*70)
        print("VISUALIZATION OPTIONS")
        print("─"*70)
        
        print("\n1. Text visualization")
        print("2. Graphic visualization")
        print("3. Both")
        print("4. Skip visualization")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice in ['1', '3']:
            TextVisualizer.display_results(results, self.current_type, 
                                          algorithm_name, start, goal)
        
        if choice in ['2', '3']:
            if self.current_type == 'graph':
                GraphVisualizer.visualize(
                    self.current_scenario,
                    results['visited'],
                    results['path'],
                    start, goal,
                    algorithm_name,
                    show=True
                )
            else:  
                MazeVisualizer.visualize(
                    self.current_scenario,
                    results['visited'],
                    results['path'],
                    start, goal,
                    algorithm_name,
                    show=True
                )
    
    def run(self):
        while True:
            self.clear_screen()
            self.print_header()
            
            scenario_type, scenario = self.select_scenario()
            self.current_type = scenario_type
            self.current_scenario = scenario
            
            algorithm_name, algorithm = self.select_algorithm()
            
            if scenario_type == 'graph':
                start, goal = self.get_start_goal_graph()
            else:
                start, goal = self.get_start_goal_maze()
            
            results = self.run_search(algorithm_name, algorithm, start, goal)
            
            self.visualize_results(results, algorithm_name, start, goal)
            
            choice = input("\nRun another search? (y/n): ").strip().lower()
            if choice != 'y':
                self.clear_screen()
                print("\n" + "Thanks for using Search Algorithms Visualization!".center(70))
                print("="*70 + "\n")
                break


def main():
    try:
        app = SearchAlgorithmApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
