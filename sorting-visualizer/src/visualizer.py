import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional

class SortingVisualizer:
    def __init__(self):
        self.fig = None
        self.ax = None
        self.canvas = None
        
    def setup_plot(self, fig, ax):
        self.fig = fig
        self.ax = ax
        
    def update_plot(self, data: List[int], highlights: Optional[List[int]] = None, 
                   title: str = "Sorting Visualization"):
        if self.ax is None:
            return
            
        self.ax.clear()
        
        colors = ['#3498db'] * len(data)
        if highlights:
            for idx in highlights:
                if 0 <= idx < len(colors):
                    colors[idx] = '#e74c3c'
        
        bars = self.ax.bar(range(len(data)), data, color=colors, alpha=0.7, edgecolor='white')
        
        # Customize the plot
        self.ax.set_facecolor('#ecf0f1')
        if hasattr(self.fig, 'patch'):
            self.fig.patch.set_facecolor('#2c3e50')
        self.ax.tick_params(colors='white')
        
        self.ax.set_title(title, fontsize=14, fontweight='bold', color='white', pad=20)
        self.ax.set_xlabel('Index', color='white', fontsize=12)
        self.ax.set_ylabel('Value', color='white', fontsize=12)
        self.ax.set_ylim(0, max(data) * 1.1)
        
        # Add value labels for smaller datasets
        if len(data) <= 50:
            for i, bar in enumerate(bars):
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{int(height)}', ha='center', va='bottom', 
                           fontsize=8, color='white', fontweight='bold')