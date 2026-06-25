
__version__ = '1.0.0'
__author__ = 'Your Name'
__description__ = 'Comprehensive search algorithm visualization and comparison tool'

from algorithms import BFS, DFS, UCS, AStar
from scenarios import Graph, Maze
from visualization import TextVisualizer, GraphVisualizer, MazeVisualizer

__all__ = [
    'BFS', 'DFS', 'UCS', 'AStar',
    'Graph', 'Maze',
    'TextVisualizer', 'GraphVisualizer', 'MazeVisualizer'
]
