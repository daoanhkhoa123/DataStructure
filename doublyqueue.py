class _DoublyLinkedBase:
    class _Node:
        __slot__ = "_key", "_prev", "_next"

        def __init__(self, key, prev, next) -> None:
            self._key = key
            self._prev = prev
            self._next = next

    def __init__(self) -> None:
        self._head = self._Node(None, None, None)
        self._tail = self._Node(None, None, None)
        self._head._next = self._tail
        self._tail._prev = self._head
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _insert_between(self, key, predecessor: _Node, successor: _Node):
        new = self._Node(key, predecessor, successor)  # head and tail are None
        predecessor._next = new
        successor._prev = new
        self._size += 1

        return new

    def _delete_node(self, node: _Node):
        predecessor = node._prev
        successor = node._next

        predecessor._next = successor
        successor._prev = predecessor

        self._size -= 1

        key = node._key
        node = None

        return key


class DoublyQueueLL(_DoublyLinkedBase):
    def first(self):
        if self.is_empty():
            raise IndexError("Doubly queue is empty")

        return self._head

    def last(self):
        if self.is_empty():
            raise IndexError("Doubly queue is empty")

        return self._tail

    def delete_first(self):
        if self.is_empty():
            raise IndexError("Doubly queue is empty")

        self._delete_node(self._head._next)  # head is constant

    def delete_last(self):
        if self.is_empty():
            raise IndexError("Doubly queue is empty")

        self._delete_node(self._tail._prev)  # head is constant

    def insert_first(self, key):
        # head and tail are None
        self._insert_between(key, self._head, self._head._next)

    def insert_last(self, key):
        self._insert_between(key, self._tail._prev, self._tail)
