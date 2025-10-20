# sorting-visualizer

A comprehensive Python application that visualizes various sorting algorithms with an intuitive graphical user interface built using Tkinter and Matplotlib.



# Features

- Sorting Algorithms        : Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, and Heap Sort
- Real-time Visualization   : Watch algorithms sort data step by step with color-coded elements
- Interactive Controls      : Adjust data size and animation speed in real-time
- Performance Comparison    : Compare all algorithms side by side with detailed statistics
- Modern Dark UI            : Clean, dark-themed interface for better viewing experience
- Educational Tool          : Perfect for understanding algorithm behavior and complexity


# Project Structure
```bash-sorting-visualizer/
  ├── src/
  │   ├── main.py              # Main application and GUI
  │   ├── sorting_algorithms.py # All sorting algorithm implementations
  │   └── visualizer.py        # Visualization utilities
  │   └── visualizer.py        # Audio Manager
  ├── tests/
  │   └── test_sorting.py      # Unit tests
  ├── requirements.txt         # Python dependencies
  ├── README.md               # Project documentation
  └── run.py                  # Application entry point
```
# Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
```bash

git clone https://github.com/amanraj914233/sorting-visualizer
cd sorting-visualizer
pip install -r requirements.txt
python run.py
```

# Usage
Select Algorithm: Choose from 6 different sorting algorithms from the dropdown
Adjust Settings:
Data Size: 10-100 elements
Speed: Control animation speed (0.01s - 0.5s per step)
Generate Data: Create new random data to sort
Start Sorting: Click "Start Sorting" to visualize the algorithm
Compare Algorithms: Use "Compare All" to see performance metrics

```bash
# Algorithms Implemented
-Algorithm	       Time Complexity	   Space Complexity    	Features
-Bubble Sort	       O(n²)            	O(1)              	Simple, educational
-Selection Sort	     O(n²)	            O(1)	              Finds minimum elements
-Insertion Sort	     O(n²)	            O(1)	              Efficient for small data
-Merge Sort	         O(n log n)	        O(n)	              Divide and conquer
-Quick Sort	         O(n log n)	        O(log n)	          Efficient average case
-Heap Sort         	O(n log n)        	O(1)	              Uses heap data structure
```
