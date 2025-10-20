import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import threading
from src.sorting_algorithms import SortingAlgorithms
from src.visualizer import SortingVisualizer

class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        self.sorting = SortingAlgorithms()
        self.visualizer = SortingVisualizer()
        
        self.data_size = tk.IntVar(value=50)
        self.speed = tk.DoubleVar(value=0.05)
        self.current_algorithm = tk.StringVar(value="Bubble Sort")
        self.is_sorting = False
        self.sorting_thread = None
        self.data = []
        
        self.setup_ui()
        self.generate_data()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        algorithms = ["Bubble Sort", "Selection Sort", "Insertion Sort", 
                     "Merge Sort", "Quick Sort", "Heap Sort"]
        algo_combo = ttk.Combobox(control_frame, textvariable=self.current_algorithm, 
                                 values=algorithms, state="readonly", width=15)
        algo_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Data size control
        ttk.Label(control_frame, text="Data Size:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        size_scale = ttk.Scale(control_frame, from_=10, to=100, variable=self.data_size, 
                              orient=tk.HORIZONTAL, length=100)
        size_scale.grid(row=0, column=3, padx=(0, 10))
        ttk.Label(control_frame, textvariable=self.data_size).grid(row=0, column=4, padx=(0, 20))
        
        # Speed control
        ttk.Label(control_frame, text="Speed:").grid(row=0, column=5, sticky=tk.W, padx=(0, 10))
        speed_scale = ttk.Scale(control_frame, from_=0.01, to=0.5, variable=self.speed, 
                               orient=tk.HORIZONTAL, length=100)
        speed_scale.grid(row=0, column=6, padx=(0, 10))
        ttk.Label(control_frame, textvariable=self.speed).grid(row=0, column=7, padx=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=8, sticky=tk.E)
        
        ttk.Button(button_frame, text="Generate Data", 
                  command=self.generate_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Start Sorting", 
                  command=self.start_sorting).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Reset", 
                  command=self.reset).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Compare All", 
                  command=self.compare_algorithms).pack(side=tk.LEFT)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=4, width=80, font=('Consolas', 10))
        self.stats_text.pack(fill=tk.X)
        
        # Visualization frame
        viz_frame = ttk.LabelFrame(main_frame, text="Visualization", padding=10)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def generate_data(self):
        if self.is_sorting:
            messagebox.showwarning("Warning", "Please wait for current sorting to complete!")
            return
            
        size = self.data_size.get()
        self.data = list(range(1, size + 1))
        random.shuffle(self.data)
        self.update_visualization()
        self.update_stats("Data generated successfully!")
        
    def update_visualization(self, highlights=None, title=None):
        self.ax.clear()
        
        colors = ['#3498db'] * len(self.data)
        if highlights:
            for idx in highlights:
                if 0 <= idx < len(colors):
                    colors[idx] = '#e74c3c'
        
        bars = self.ax.bar(range(len(self.data)), self.data, color=colors, alpha=0.7, edgecolor='white')
        
        # Customize the plot
        self.ax.set_facecolor('#ecf0f1')
        self.fig.patch.set_facecolor('#2c3e50')
        
        for spine in self.ax.spines.values():
            spine.set_color('white')
            
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        
        if title:
            self.ax.set_title(title, fontsize=14, fontweight='bold', color='white', pad=20)
        else:
            self.ax.set_title(f"{self.current_algorithm.get()} - Ready to Sort", 
                            fontsize=14, fontweight='bold', color='white', pad=20)
        
        self.ax.set_xlabel('Index', color='white', fontsize=12)
        self.ax.set_ylabel('Value', color='white', fontsize=12)
        self.ax.set_ylim(0, max(self.data) * 1.1)
        
        #
        if len(self.data) <= 50:
            for i, bar in enumerate(bars):
                height = bar.get_height()
                # Use black text
                text_color = 'black' if colors[i] == '#3498db' else 'white'
                self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{int(height)}', ha='center', va='bottom', 
                           fontsize=8, color=text_color, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7))
        
        self.canvas.draw()
        
    def update_stats(self, message):
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"{message}\n")
        self.stats_text.insert(tk.END, f"Data Size: {len(self.data)}\n")
        self.stats_text.insert(tk.END, f"Current Algorithm: {self.current_algorithm.get()}\n")
        self.stats_text.insert(tk.END, f"Speed: {self.speed.get():.2f} seconds")
        
    def start_sorting(self):
        if self.is_sorting:
            messagebox.showwarning("Warning", "Sorting already in progress!")
            return
            
        algorithm = self.current_algorithm.get()
        self.is_sorting = True
        
        # Run sorting in a separate thread to keep UI responsive
        self.sorting_thread = threading.Thread(target=self.run_sorting_algorithm, args=(algorithm,))
        self.sorting_thread.daemon = True
        self.sorting_thread.start()
        
    def run_sorting_algorithm(self, algorithm):
        try:
            start_time = time.time()
            steps_generator = None
            
            if algorithm == "Bubble Sort":
                steps_generator = self.sorting.bubble_sort(self.data.copy())
            elif algorithm == "Selection Sort":
                steps_generator = self.sorting.selection_sort(self.data.copy())
            elif algorithm == "Insertion Sort":
                steps_generator = self.sorting.insertion_sort(self.data.copy())
            elif algorithm == "Merge Sort":
                steps_generator = self.sorting.merge_sort(self.data.copy())
            elif algorithm == "Quick Sort":
                steps_generator = self.sorting.quick_sort(self.data.copy())
            elif algorithm == "Heap Sort":
                steps_generator = self.sorting.heap_sort(self.data.copy())
            else:
                steps_generator = self.sorting.bubble_sort(self.data.copy())
            
            # Animate the sorting steps
            for step_data, highlights, comparisons, swaps in steps_generator:
                if not self.is_sorting:  
                    break
                    
                self.data = step_data
                title = f"{algorithm} - Comparisons: {comparisons}, Swaps: {swaps}"
                self.root.after(0, lambda: self.update_visualization(highlights, title))
                time.sleep(self.speed.get())
            
            elapsed_time = time.time() - start_time
            final_message = f"{algorithm} completed in {elapsed_time:.2f} seconds"
            self.root.after(0, lambda: self.update_stats(final_message))
            
        except Exception as e:
            #
            error_msg = str(e)
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("Error", f"An error occurred: {msg}"))
        finally:
            self.is_sorting = False
            
    def reset(self):
        self.is_sorting = False
        self.generate_data()
        
    def compare_algorithms(self):
        CompareWindow(self.root, self.data_size.get())

class CompareWindow:
    def __init__(self, parent, data_size):
        self.window = tk.Toplevel(parent)
        self.window.title("Algorithm Comparison")
        self.window.geometry("1000x700")
        self.window.configure(bg='#2c3e50')
        
        self.data_size = data_size
        self.sorting = SortingAlgorithms()
        
        self.setup_ui()
        self.run_comparison()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Comparison Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(results_frame, height=20, width=80, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Close", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
        
    def run_comparison(self):
        algorithms = ["Bubble Sort", "Selection Sort", "Insertion Sort", 
                     "Merge Sort", "Quick Sort", "Heap Sort"]
        
        results = []
        
        for algo in algorithms:
            # Generate test data
            test_data = list(range(1, self.data_size + 1))
            random.shuffle(test_data)
            
            start_time = time.time()
            
            try:
                if algo == "Bubble Sort":
                    steps = list(self.sorting.bubble_sort(test_data.copy()))
                elif algo == "Selection Sort":
                    steps = list(self.sorting.selection_sort(test_data.copy()))
                elif algo == "Insertion Sort":
                    steps = list(self.sorting.insertion_sort(test_data.copy()))
                elif algo == "Merge Sort":
                    steps = list(self.sorting.merge_sort(test_data.copy()))
                elif algo == "Quick Sort":
                    steps = list(self.sorting.quick_sort(test_data.copy()))
                elif algo == "Heap Sort":
                    steps = list(self.sorting.heap_sort(test_data.copy()))
                
                elapsed_time = time.time() - start_time
                
                # Get final statistics
                if steps:
                    final_comparisons = steps[-1][2]
                    final_swaps = steps[-1][3]
                else:
                    final_comparisons = final_swaps = 0
                    
                results.append({
                    'algorithm': algo,
                    'time': elapsed_time,
                    'comparisons': final_comparisons,
                    'swaps': final_swaps
                })
                
            except Exception as e:
                results.append({
                    'algorithm': algo,
                    'time': 0,
                    'comparisons': 0,
                    'swaps': 0,
                    'error': str(e)
                })
            
        # Display results
        self.display_results(results)
        
    def display_results(self, results):
        self.results_text.delete(1.0, tk.END)
        
        # Sort by execution time
        results.sort(key=lambda x: x['time'])
        
        self.results_text.insert(tk.END, "ALGORITHM COMPARISON RESULTS\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.results_text.insert(tk.END, f"Data Size: {self.data_size}\n\n")
        
        for i, result in enumerate(results, 1):
            if 'error' in result:
                self.results_text.insert(tk.END, 
                    f"{i}. {result['algorithm']:15} | "
                    f"ERROR: {result['error']}\n")
            else:
                self.results_text.insert(tk.END, 
                    f"{i}. {result['algorithm']:15} | "
                    f"Time: {result['time']:6.3f}s | "
                    f"Comparisons: {result['comparisons']:6} | "
                    f"Swaps: {result['swaps']:6}\n")

def main():
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()