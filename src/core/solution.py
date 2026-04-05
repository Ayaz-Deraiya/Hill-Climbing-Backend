from copy import deepcopy

class Solution:
    def __init__(self, bins):
        self.bins = bins

    def clone(self):
        return deepcopy(self)

    def cost(self):
        return len(self.bins)