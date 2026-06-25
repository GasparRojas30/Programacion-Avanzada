from typing import List, Tuple, Optional
import math


class Maze:
    
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
    
    def is_valid_position(self, row: int, col: int) -> bool:
        return (0 <= row < self.rows and 
                0 <= col < self.cols and 
                self.grid[row][col] == 0)
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        row, col = pos
        neighbors = []
        
        # 4-directional movement
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def get_neighbors_with_cost(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        neighbors = self.get_neighbors(pos)
        return [(n, 1.0) for n in neighbors]
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def euclidean_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return math.sqrt(dx * dx + dy * dy)
    
    def is_solvable(self, start: Tuple[int, int], goal: Tuple[int, int]) -> bool:
        if not self.is_valid_position(start[0], start[1]):
            return False
        if not self.is_valid_position(goal[0], goal[1]):
            return False
        
        from collections import deque
        queue = deque([start])
        visited = {start}
        
        while queue:
            pos = queue.popleft()
            if pos == goal:
                return True
            
            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False
    
    @staticmethod
    def create_example_maze() -> 'Maze':
        grid = [
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        ]
        return Maze(grid)
    
    def load_from_file(self, filename: str):
        with open(filename, 'r') as f:
            self.grid = []
            for line in f:
                row = [int(ch) for ch in line.strip() if ch in '01']
                if row:
                    self.grid.append(row)
            
            self.rows = len(self.grid)
            self.cols = len(self.grid[0]) if self.grid else 0
    
    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            for row in self.grid:
                f.write(''.join(str(cell) for cell in row) + '\n')
