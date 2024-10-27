class HeapPiortyQueue:
    """Min-oriented priority queue implemented with a binary heap"""

    class _Item:
        __slot__ = "_value", "_key"

        def __init__(self, key, value) -> None:
            self._key = key
            self._value = value

        def __lt__(self, __other: object) -> bool:  # flip side if you want min heap
            return self._value < __other._value

        def __eq__(self, __other: object) -> bool:
            return self._value == __other._value

        def __ge__(self, __other: object) -> bool:  # flip side if you want min heap
            return self._value >= __other._value

    def __init__(self) -> None:
        self._data = list()

    """ PRIVATE """
    # ------ INDEXING ---------

    def _parent(self, i: int):
        return (i - 1) // 2

    def _left(self, i: int):
        return i * 2 + 1

    def _right(self, i: int):
        return i * 2 + 2

    def _has_left(self, i: int):
        return self._left(i) < len(self)

    def _has_right(self, i: int):
        return self._right(i) < len(self)

    def _swap(self, i: int, ii: int):
        self._data[i], self._data[ii] = self._data[ii], self._data[i]

    # -------- HEAP ---------------------
    def _upheap(self, i):
        # avoid i = -1
        while i > 0 and self._data[self._parent(i)] >= self._data[i]:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _downheap(self, i):
        while True:
            min = self._left(i) if self._has_left(i) else None  # default min left

            # if right is smaller
            if self._has_right(i) and (
                min is None or self._data[self._right(i)] <= self._data[min]
            ):
                min = self._right(i)

            if min is None or self._data[i] <= self._data[min]:
                break

            self._swap(i, min)
            i = min

    """ PUBLIC """

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self) == 0

    # -------
    def add(self, key, value):
        self._data.append(self._Item(key, value))
        self._upheap(len(self) - 1)

    def min(self):
        """Return the (k,v) pair with smallest v"""
        if self.is_empty():
            raise ValueError("Piority queue is empty")

        return self._data[0]._key, self._data[0]._value

    def remove_min(self):
        """Remove and return the (k,v) pair with smallest v"""
        if self.is_empty():
            raise ValueError("Piority queue is empty")

        self._swap(0, len(self) - 1)
        item = self._data.pop()  # has to

        self._downheap(0)
        return item._key, item._value


class HeapPriorityQueueAdaptive(HeapPiortyQueue):
    """A locator-based priority queue implemented with a binary heap"""

    # ------------------------------ nested Locator class ------------------------------
    class _Locator(HeapPiortyQueue._Item):
        __slot__ = "_index"

        def __init__(self, key, value, index) -> None:
            super().__init__(key, value)
            self._index = index

    def __init__(self) -> None:
        super().__init__()

    """ PRIVATE """

    # override swap
    def _swap(self, i, ii):
        super()._swap(i, ii)
        # index should correspond to its place
        self._data[i]._index = i
        self._data[ii]._index = ii

    def _bubble(self, i):
        if i > 0 and self._data[i] < self._data[self._parent(i)]:
            self._upheap(i)
        else:
            self._downheap(i)

    """ PUBLIC """

    def add(self, key, value) -> _Locator:
        """Add and return a key-value pair"""
        token = self._Locator(key, value, len(self))  # for return function
        self._data.append(token)

        self._upheap(len(self) - 1)
        return token

    def update(self, locator, key, value) -> _Locator:
        """Update the key and value for the entry identified by Locator locator"""
        if (
            locator._index < 0
            or locator._index >= len(self)
            or self._data[locator._index] is not locator
        ):
            raise ValueError("Invalid locator")

        locator._key = key
        locator._value = value
        self._bubble(locator._index)
        return locator

    def remove(self, locator) -> tuple:
        """Remove and return the (k,v) pair identified by Locator locator"""
        if (
            locator._index < 0
            or locator._index >= len(self)
            or self._data[locator._index] is not locator
        ):
            raise ValueError("Invalid locator")

        if locator._index == len(self) - 1:  # is leaf
            return self._data.pop()

        old_i = locator._index
        self._swap(locator._index, len(self) - 1)
        token = self._data.pop()  # for return function

        self._bubble(old_i)
        return token._key, token._value  # because it no longer in queue


if __name__ == "__main__":
    q = HeapPriorityQueueAdaptive()
    for i in [int(x) for x in "19 2 63 52 47 6 3 18 33".split()]:
        q.add(i, i)

    print(*[x._key for x in q._data])
    print(q.remove_min())
    print(q.remove_min())
    print(q.remove_min())
    print(q.remove_min())
    print(q.remove_min())
