from doublyqueue import _DoublyLinkedBase


class PositionalList(_DoublyLinkedBase):
    """A sequential container of elements allowing positional access."""

    # -------------------------- nested Position class --------------------------
    class Position:
        def __init__(self, container, node: _DoublyLinkedBase._Node) -> None:
            self._container = container
            self._node = node

        def get_key(self):
            return self._node._key

        def __eq__(self, __value: object) -> bool:
            return type(self) is type(__value) and __value._node is self._node

        def __ne__(self, __value: object) -> bool:
            return not (self == __value)

    def __init__(self) -> None:
        super().__init__()
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)

        self._header._next = self._trailer
        self._trailer._prev = self._header

    # ------------------------------- utility method -------------------------------
    def _validate(self, position):
        if not isinstance(position, self.Position):
            raise TypeError("p muse be proper Position type")

        if position._container is not self:
            raise ValueError("p does not belong to this container")

        if position._node._next is None:
            raise ValueError("p is no longer valid")

        return position._node

    def _make_position(self, node):
        if node is self._header or node is self._trailer:
            return None

        else:
            return self.Position(self, node)

    # ------------------------------- accessors -------------------------------
    def first(self):
        return self._make_position(self._header._next)

    def last(self):
        return self._make_position(self._trailer._prev)

    def before(self, position):
        return self._make_position(self._validate(position)._prev)

    def after(self, position):
        return self._make_position(self._validate(position)._next)

    def __iter__(self):
        cursor = self.first()
        while cursor:
            yield cursor.get_key()
            cursor = self.after(cursor)

    def _insert_between(self, key, predecessor: _DoublyLinkedBase._Node, successor: _DoublyLinkedBase._Node):
        self._make_position(super()._insert_between(
            key, predecessor, successor))

    # ------------------------------- mutators -------------------------------
    # override inherited version to return Position, rather than Node

    def add_first(self, key):
        return self._insert_between(key, self._header, self._header._next)

    def add_last(self, key):
        return self._insert_between(key, self._trailer._prev, self._trailer)

    def add_before(self, position, key):
        """Insert element e into list before Position p and return new Position."""
        original = self._validate(position)
        return self._insert_between(key, original._prev, original)

    def add_after(self, position, key):
        """Insert element e into list after Position p and return new Position"""
        original = self._validate(position)
        return self._insert_between(key, original, original._next)

    def delete(self, position):
        """Remove and return the element at Position p"""
        original = self._validate(position)
        return self._delete_node(original)

    def replace(self, position, key):
        """
        Replace the element at Position p with e.

        Return the element formerly at Position p.
        """
        original = self._validate(position)
        original_value = original._key
        original._key = key
        return original_value
