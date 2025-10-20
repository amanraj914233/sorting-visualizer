import random
from typing import List, Tuple, Generator

class SortingAlgorithms:
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        
    def reset_counters(self):
        self.comparisons = 0
        self.swaps = 0
        
    def bubble_sort(self, data: List[int]) -> Generator[Tuple[List[int], List[int], int, int], None, None]:
        """Bubble Sort algorithm with step-by-step yield"""
        self.reset_counters()
        n = len(data)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                self.comparisons += 1
                yield data.copy(), [j, j+1], self.comparisons, self.swaps
                
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    self.swaps += 1
                    swapped = True
                    yield data.copy(), [j, j+1], self.comparisons, self.swaps
            
            if not swapped:
                break
                
        yield data.copy(), [], self.comparisons, self.swaps
        
    def selection_sort(self, data: List[int]) -> Generator[Tuple[List[int], List[int], int, int], None, None]:
        """Selection Sort algorithm with step-by-step yield"""
        self.reset_counters()
        n = len(data)
        
        for i in range(n):
            min_idx = i
            yield data.copy(), [i, min_idx], self.comparisons, self.swaps
            
            for j in range(i + 1, n):
                self.comparisons += 1
                yield data.copy(), [i, j, min_idx], self.comparisons, self.swaps
                
                if data[j] < data[min_idx]:
                    min_idx = j
                    yield data.copy(), [i, j, min_idx], self.comparisons, self.swaps
            
            if min_idx != i:
                data[i], data[min_idx] = data[min_idx], data[i]
                self.swaps += 1
                yield data.copy(), [i, min_idx], self.comparisons, self.swaps
                
        yield data.copy(), [], self.comparisons, self.swaps
        
    def insertion_sort(self, data: List[int]) -> Generator[Tuple[List[int], List[int], int, int], None, None]:
        """Insertion Sort algorithm with step-by-step yield"""
        self.reset_counters()
        
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            yield data.copy(), [i, j], self.comparisons, self.swaps
            
            while j >= 0 and data[j] > key:
                self.comparisons += 1
                data[j + 1] = data[j]
                self.swaps += 1
                j -= 1
                yield data.copy(), [i, j+1], self.comparisons, self.swaps
                
            data[j + 1] = key
            self.swaps += 1
            yield data.copy(), [j+1], self.comparisons, self.swaps
            
        yield data.copy(), [], self.comparisons, self.swaps
        
    def merge_sort(self, data: List[int]) -> Generator[Tuple[List[int], List[int], int, int], None, None]:
        """Merge Sort algorithm with step-by-step yield"""
        self.reset_counters()
        
        def merge_sort_helper(arr, left, right):
            if left < right:
                mid = (left + right) // 2
                yield from merge_sort_helper(arr, left, mid)
                yield from merge_sort_helper(arr, mid + 1, right)
                yield from merge(arr, left, mid, right)
                
        def merge(arr, left, mid, right):
            left_arr = arr[left:mid+1]
            right_arr = arr[mid+1:right+1]
            
            i = j = 0
            k = left
            
            while i < len(left_arr) and j < len(right_arr):
                self.comparisons += 1
                yield arr.copy(), [k], self.comparisons, self.swaps
                
                if left_arr[i] <= right_arr[j]:
                    arr[k] = left_arr[i]
                    i += 1
                else:
                    arr[k] = right_arr[j]
                    j += 1
                    self.swaps += 1
                k += 1
                
            while i < len(left_arr):
                arr[k] = left_arr[i]
                i += 1
                k += 1
                self.swaps += 1
                yield arr.copy(), [k-1], self.comparisons, self.swaps
                
            while j < len(right_arr):
                arr[k] = right_arr[j]
                j += 1
                k += 1
                self.swaps += 1
                yield arr.copy(), [k-1], self.comparisons, self.swaps
                
            yield arr.copy(), list(range(left, right+1)), self.comparisons, self.swaps
                
        yield from merge_sort_helper(data, 0, len(data) - 1)
        yield data.copy(), [], self.comparisons, self.swaps
        
    def quick_sort(self, data: List[int]) -> Generator[Tuple[List[int], List[int], int, int], None, None]:
        """Quick Sort algorithm with step-by-step yield"""
        self.reset_counters()
        
        def quick_sort_helper(arr, low, high):
            if low < high:
                pi = yield from partition(arr, low, high)
                yield from quick_sort_helper(arr, low, pi - 1)
                yield from quick_sort_helper(arr, pi + 1, high)
                
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                self.comparisons += 1
                yield arr.copy(), [j, high, i], self.comparisons, self.swaps
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    if i != j:
                        self.swaps += 1
                    yield arr.copy(), [i, j, high], self.comparisons, self.swaps
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            if i + 1 != high:
                self.swaps += 1
            yield arr.copy(), [i+1, high], self.comparisons, self.swaps
            
            return i + 1
            
        yield from quick_sort_helper(data, 0, len(data) - 1)
        yield data.copy(), [], self.comparisons, self.swaps
        
    def heap_sort(self, data: List[int]) -> Generator[Tuple[List[int], List[int], int, int], None, None]:
        """Heap Sort algorithm with step-by-step yield"""
        self.reset_counters()
        n = len(data)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            yield from self.heapify(data, n, i)
            
        # Extract elements from heap
        for i in range(n - 1, 0, -1):
            data[i], data[0] = data[0], data[i]
            self.swaps += 1
            yield data.copy(), [i, 0], self.comparisons, self.swaps
            yield from self.heapify(data, i, 0)
            
        yield data.copy(), [], self.comparisons, self.swaps
        
    def heapify(self, arr, n, i):
        """Helper function for heap sort"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            self.comparisons += 1
            yield arr.copy(), [i, left, largest], self.comparisons, self.swaps
            if arr[left] > arr[largest]:
                largest = left
                
        if right < n:
            self.comparisons += 1
            yield arr.copy(), [i, right, largest], self.comparisons, self.swaps
            if arr[right] > arr[largest]:
                largest = right
                
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.swaps += 1
            yield arr.copy(), [i, largest], self.comparisons, self.swaps
            yield from self.heapify(arr, n, largest)