from copy import deepcopy

class Solution:
    def __init__(self, bins):
        self.bins = bins

    def clone(self):
        return deepcopy(self)

    def cost(self):
        cost = len(self.bins)
        for b in self.bins:
            cost += (b.capacity - b.used) ** 2
        return cost
