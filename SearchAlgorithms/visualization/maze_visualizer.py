import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import List, Tuple


class MazeVisualizer:

    
    @staticmethod
    def visualize(maze: Any, visited: List[Tuple[int, int]], 
                  path: List[Tuple[int, int]], start: Tuple[int, int], 
                  goal: Tuple[int, int], algorithm_name: str = "Unknown",
                  save_path: str = None, show: bool = True):
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        rows, cols = maze.rows, maze.cols
        visual_grid = np.ones((rows, cols, 3))  # RGB
        
        for i in range(rows):
            for j in range(cols):
                if maze.grid[i][j] == 1:  # Barrier
                    visual_grid[i][j] = [0, 0, 0]  # Black
                else:
                    visual_grid[i][j] = [1, 1, 1]  # White
        
        visited_set = set(visited)
        for idx, (i, j) in enumerate(visited):
            intensity = 1.0 - (idx / max(len(visited), 1)) * 0.7  # Fade effect
            visual_grid[i][j] = [0.3, 0.7, intensity]  # Light blue
        
        for pos in path:
            if pos != start and pos != goal:
                visual_grid[pos[0]][pos[1]] = [1, 1, 0.2]  # Yellow
        
        if start[0] < rows and start[1] < cols:
            visual_grid[start[0]][start[1]] = [0, 1, 0]  # Green
        
        if goal[0] < rows and goal[1] < cols:
            visual_grid[goal[0]][goal[1]] = [1, 0, 0]  # Red
        
        # Display grid
        ax.imshow(visual_grid)
        
        # Draw grid lines
        for i in range(rows + 1):
            ax.axhline(i - 0.5, color='gray', linewidth=0.5, alpha=0.3)
        for j in range(cols + 1):
            ax.axvline(j - 0.5, color='gray', linewidth=0.5, alpha=0.3)
        
        # Draw path with arrows
        if len(path) > 1:
            for k in range(len(path) - 1):
                y1, x1 = path[k]
                y2, x2 = path[k + 1]
                ax.arrow(x1, y1, (x2 - x1) * 0.4, (y2 - y1) * 0.4,
                        head_width=0.3, head_length=0.2, fc='darkgreen', 
                        ec='darkgreen', linewidth=2, alpha=0.8)
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', label='Start'),
            Patch(facecolor='red', label='Goal'),
            Patch(facecolor='yellow', label='Path'),
            Patch(facecolor='lightblue', label='Visited'),
            Patch(facecolor='white', label='Free'),
            Patch(facecolor='black', label='Barrier')
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        # Info text
        info_text = f"Algorithm: {algorithm_name}\n"
        info_text += f"Maze Size: {rows}×{cols}\n"
        info_text += f"Path Length: {len(path)}\n"
        info_text += f"Visited Cells: {len(visited)}\n"
        info_text += f"Success: {'Yes' if len(path) > 0 else 'No'}"
        
        ax.text(0.98, 0.02, info_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
        
        ax.set_title(f"Maze Search Visualization - {algorithm_name}",
                    fontsize=14, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Maze visualization saved to: {save_path}")
        
        if show:
            plt.show()
        
        return fig, ax
