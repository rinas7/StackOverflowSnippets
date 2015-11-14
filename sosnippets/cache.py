class Cache(object):

    def __init__(self, max_items):
        self.max_items = max_items
        self.items = []

    def add(self, key, item):
        for i, (k, _) in enumerate(self.items):
            if k == key:
                del self.items[i]
                break
        self.items.append((key, item))
        while len(self.items) > self.max_items:
            del self.items[0]

    def get(self, key):
        for k, item in self.items:
            if k == key:
                return item
        return None
