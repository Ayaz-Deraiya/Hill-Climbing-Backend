import random
from src.core.solution import Solution
from src.core.bin import Bin

class HillClimbing:

    def __init__(self, capacity):
        self.capacity = capacity

    def initial_solution(self, items):
        bins = []
        for item in items:
            placed = False
            for b in bins:
                if b.can_fit(item):
                    b.add(item)
                    placed = True
                    break
            if not placed:
                new_bin = Bin(self.capacity)
                new_bin.add(item)
                bins.append(new_bin)
        return Solution(bins)

    def generate_neighbor(self, solution):
        new_solution = solution.clone()

        if not new_solution.bins:
            return new_solution

        b1 = random.choice(new_solution.bins)
        if not b1.items:
            return new_solution

        item = random.choice(b1.items)
        b1.remove(item)

        b2 = random.choice(new_solution.bins)

        if b2.can_fit(item):
            b2.add(item)
        else:
            new_bin = Bin(self.capacity)
            new_bin.add(item)
            new_solution.bins.append(new_bin)

        new_solution.bins = [b for b in new_solution.bins if b.items]

        return new_solution

    def optimize(self, items, max_iter=1000):
        current = self.initial_solution(items)
        history = [current.cost()]

        for _ in range(max_iter):
            neighbor = self.generate_neighbor(current)
            if neighbor.cost() < current.cost():
                current = neighbor
            history.append(current.cost())

        return current, history
