class Parition:
    class _Poisition:
        """Create a new position that is the leader of its own group."""

        def __init__(self, container, key) -> None:
            self.container = container  # reference to Partition instance
            self._key = key
            self._size = 1
            self._parent = self  # convention for group leader

        def get_key(self):
            return self._key

    def make_group(self, key):
        """Makes a new group containing element e, and returns its Position"""
        return self._Poisition(self, key)

    def find(self, position):
        """Finds the group containging p and return the position of its leader"""
        while position._parent is not position:
            position = position._parent

        return position

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a._size < b._size:
            b._size += a._size
            a._parent = b

        else:
            a._size += b._size
            b._parent = a
