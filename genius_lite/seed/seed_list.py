class SeedList:
    _list = []

    def push(self, seed):
        self._list.append(seed)

    def pop(self):
        return self._list.pop() if self.length else None

    @property
    def length(self):
        return len(self._list)
