class Bin:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.used = 0

    def can_fit(self, item):
        return self.used + item <= self.capacity

    def add(self, item):
        self.items.append(item)
        self.used += item

    def remove(self, item):
        self.items.remove(item)
        self.used -= item
