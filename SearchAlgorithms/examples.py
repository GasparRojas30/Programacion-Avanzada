from algorithms import BFS, DFS, UCS, AStar
from scenarios import Graph, Maze
from visualization import TextVisualizer, GraphVisualizer, MazeVisualizer


def example_graph_search():
    print("\n" + "="*70)
    print("EXAMPLE 1: Graph Search")
    print("="*70)
    
    graph = Graph.create_example_graph()
    
    start, goal = 'A', 'F'
    
    algorithms = [
        ('BFS', BFS()),
        ('DFS', DFS()),
        ('UCS', UCS()),
    ]
    
    for algo_name, algo in algorithms:
        print(f"\n{algo_name}:")
        results = algo.search(graph, start, goal)
        TextVisualizer.display_results(results, 'Graph', algo_name, start, goal)


def example_maze_search():
    print("\n" + "="*70)
    print("EXAMPLE 2: Maze Search")
    print("="*70)
    
    # Create maze
    maze = Maze.create_example_maze()
    
    start = (0, 0)
    goal = (9, 9)
    
    if not maze.is_solvable(start, goal):
        print("Maze is not solvable from start to goal!")
        return
    
    algorithms = [
        ('BFS', BFS()),
        ('DFS', DFS()),
        ('A*', AStar()),
    ]
    
    for algo_name, algo in algorithms:
        print(f"\n{algo_name}:")
        
        if algo_name == 'A*':
            results = algo.search(maze, start, goal, maze.manhattan_distance)
        else:
            results = algo.search(maze, start, goal)
        
        TextVisualizer.display_results(results, 'Maze', algo_name, start, goal)


def example_comparison():
    print("\n" + "="*70)
    print("EXAMPLE 3: Algorithm Comparison")
    print("="*70)
    
    maze = Maze.create_example_maze()
    start = (0, 0)
    goal = (9, 9)
    
    algorithms = [
        ('BFS', BFS()),
        ('DFS', DFS()),
        ('UCS', UCS()),
        ('A*', AStar()),
    ]
    
    results_list = []
    
    for algo_name, algo in algorithms:
        if algo_name == 'A*':
            results = algo.search(maze, start, goal, maze.manhattan_distance)
        else:
            results = algo.search(maze, start, goal)
        
        results_list.append((algo_name, results))
    
    print("\n" + "─"*70)
    print("COMPARISON TABLE")
    print("─"*70)
    print(f"{'Algorithm':<12} {'Success':<10} {'Path':<8} {'Visited':<10} {'Expanded':<10}")
    print("─"*70)
    
    for algo_name, results in results_list:
        success = "✓" if results['success'] else "✗"
        path_len = len(results['path'])
        visited = len(results['visited'])
        expanded = results['nodes_expanded']
        print(f"{algo_name:<12} {success:<10} {path_len:<8} {visited:<10} {expanded:<10}")


if __name__ == "__main__":
    example_graph_search()
    example_maze_search()
    example_comparison()
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70 + "\n")
