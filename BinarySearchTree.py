class BinarySearchTree:
    def __init__(self, key=None) -> None:
        self.key = key
        self._left = None
        self._right = None

    def __str__(self):
        return str(self.key)

    # for insert with no duplicate, please iterate through set
    def insert(self, data: float):
        """Insert data

        Args:
            data (float)
        """

        if self.key is None:
            self.key = data
            return

        if data < self.key:
            if self._left is None:
                self._left = BinarySearchTree(data)
                return self._left

            else:
                return self._left.insert(data)

        else:
            if self._right is None:
                self._right = BinarySearchTree(data)
                return self._right

            else:
                return self._right.insert(data)

    def preorder(self):
        yield self.key
        if self._left:
            self._left.preorder()

        if self._right:
            self._right.preorder()

    def inorder(self):
        if self._left:
            self._left.inorder()

        yield self.key
        if self._right:
            self._right.inorder()

    def postorder(self):
        if self._left:
            self._left.postorder()

        if self._right:
            self._right.postorder()

        yield self.key

    def recur_search(self, key):
        if self.key is None:  # Empty tree
            return None

        if key == self.key:
            return self

        elif key < self.key:  # Must be on the left subtree
            if self._left:  # If there still left node
                return self._left.search(key)

        else:  # Must be on the right subtree
            if self._right:  # If there still right node
                return self._right.search(key)

    def search(self, key):
        if self.key is None:  # Empty tree
            return None

        pointer = self
        while pointer is not None:
            if key == pointer.key:
                return pointer

            elif key < pointer.key:  # Must be on the left subtree
                pointer = pointer._left

            elif key > pointer.key:  # Must be on the right subtree
                pointer = pointer._right

    def max(self):
        if self.key is None:  # Empty tree
            return None

        while self._right:
            self = self._right

        return self

    def min(self):
        if self is None or self.key is None:  # Empty tree
            return None

        while self._left:
            self = self._left

        return self

    def breathfirst_search(self):
        node = self
        from queue import Queue as Q

        queu = Q()
        queu.put(node)

        while not queu.empty:
            n = queu.get()
            print(n.data)

            queu.put(n.left)
            queu.put(n.right)

    def delete(self, key):
        if self is None or self.key is None:
            return self

        if key > self.key:
            self._right = self._right.delete(key) if self._right else self._right
            return self

        elif key < self.key:
            self._left = self._left.delete(key) if self._left else self._left
            return self

        elif key == self.key:
            if self._right is None:
                return self._left

            elif self._left is None:
                return self._right

        self.key = self._right.min_node.key
        self._right = self._right.delete(self.key)
        return self

    def book_indent(self, depth=0):
        print(" " * depth, self.key)

        if self._left is not None:
            self._left.book_indent(depth + 1)

        if self._right is not None:
            self._right.book_indent(depth + 1)

    def parenthesize(self, parenthesize_code="("):

        if parenthesize_code == "(":
            pass
        if self._left is not None:
            self._left.parenthesize("(")

        if self._right is not None:
            self._right.parenthesize(")")
