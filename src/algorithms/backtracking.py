from src.core.solution import Solution
from src.core.bin import Bin
import time

class BacktrackingBinPacking:
    def __init__(self, capacity):
        self.capacity = capacity
        self.best = float('inf')
        self.best_bins = []

    def optimize(self, items):
        start_time = time.perf_counter()
        
        sorted_items = sorted(items, reverse=True)
        self.best = len(sorted_items)
        self.best_bins = [[item] for item in sorted_items]
        
        current_bins = []
        self._backtrack(sorted_items, 0, current_bins)
        
        final_bins = []
        for bin_items in self.best_bins:
            b = Bin(self.capacity)
            for item in bin_items:
                b.add(item)
            final_bins.append(b)
            
        solution = Solution(final_bins)
        history = [solution.cost()]
        
        return solution, history

    def _backtrack(self, items, index, current_bins):
        if index == len(items):
            if len(current_bins) < self.best:
                self.best = len(current_bins)
                self.best_bins = [list(b) for b in current_bins]
            return

        if len(current_bins) >= self.best:
            return

        item = items[index]

        for i in range(len(current_bins)):
            bin_sum = sum(current_bins[i])
            if bin_sum + item <= self.capacity:
                current_bins[i].append(item)
                self._backtrack(items, index + 1, current_bins)
                current_bins[i].pop()

        current_bins.append([item])
        self._backtrack(items, index + 1, current_bins)
        current_bins.pop()
