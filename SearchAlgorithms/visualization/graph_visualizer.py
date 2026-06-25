import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
from typing import List, Dict, Any, Tuple


class GraphVisualizer:
    
    @staticmethod
    def visualize(graph: Any, visited: List[str], path: List[str], 
                  start: str, goal: str, algorithm_name: str = "Unknown",
                  save_path: str = None, show: bool = True):
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        
        G = nx.Graph()
        
        for node in graph.get_nodes():
            G.add_node(node)
        
        for node in graph.get_nodes():
            for neighbor, cost in graph.get_neighbors_with_cost(node):
                G.add_edge(node, neighbor, weight=cost)
        
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        nx.draw_networkx_edges(G, pos, ax=ax, width=2, alpha=0.5, edge_color='gray')
        
        edge_labels = {(u, v): f"{d['weight']:.1f}" 
                      for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax, font_size=8)
        
        node_colors = []
        for node in G.nodes():
            if node == start:
                node_colors.append('green')
            elif node == goal:
                node_colors.append('red')
            elif node in path:
                node_colors.append('yellow')
            elif node in visited:
                node_colors.append('lightblue')
            else:
                node_colors.append('white')
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax, 
                              node_size=1500, edgecolors='black', linewidths=2)
        
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
        
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                x1, y1 = pos[path[i]]
                x2, y2 = pos[path[i + 1]]
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', lw=2.5, 
                                         color='darkgreen', alpha=0.7))
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', edgecolor='black', label='Start'),
            Patch(facecolor='red', edgecolor='black', label='Goal'),
            Patch(facecolor='yellow', edgecolor='black', label='Path'),
            Patch(facecolor='lightblue', edgecolor='black', label='Visited'),
            Patch(facecolor='white', edgecolor='black', label='Not Visited')
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        info_text = f"Algorithm: {algorithm_name}\n"
        info_text += f"Path Cost: {len(path) - 1 if path else 'N/A'}\n"
        info_text += f"Visited: {len(visited)} nodes\n"
        info_text += f"Path Length: {len(path)} steps"
        
        ax.text(0.98, 0.02, info_text, transform=ax.transAxes, 
               fontsize=9, verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.set_title(f"Graph Search Visualization - {algorithm_name}", 
                    fontsize=14, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Graph visualization saved to: {save_path}")
        
        if show:
            plt.show()
        
        return fig, ax
