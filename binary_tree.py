class BinaryTree:
    def __init__(self, key=None) -> None:
        self.key = key
        self._left = None
        self._right = None

    def __str__(self):
        return str(self.key)

    def insert(self, data: float):
        """Insert data
        :returns BinaryTree
        """

        if self.key is None:
            self.key = data
            return

        if data < self.key:
            if self._left is None:
                self._left = BinaryTree(data)
                return self._left

            else:
                self._left.insert(data)

        else:
            if self._right is None:
                self._right = BinaryTree(data)
                return self._right

            else:
                self._right.insert(data)

    def delete(self, key):
        """:returns BinaryTree"""
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

        self.key = self._left.max_node().key
        self._left = self._left.delete(self.key)
        return self

    """ TRAVERSAL """

    def preorder(self):
        yield (self.key)
        if self._left:
            yield from self._left.preorder()

        if self._right:
            yield from self._right.preorder()

    def inorder(self):
        if self._left:
            yield from self._left.inorder()

        yield (self.key)
        if self._right:
            yield from self._right.inorder()

    def postorder(self):
        if self._left:
            yield from self._left.postorder()

        if self._right:
            yield from self._right.postorder()

        yield (self.key)

    def breathfirst(self):
        node = self
        q = [node]

        while q:
            n = q.pop(0)
            yield n.key

            q.append(n._left)
            q.append(n._right)

    """ SEARCH SINGLE """

    def recur_search(self, key):
        """:returns BinaryTree"""
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
        """:returns BinaryTree"""
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

    def max_node(self):
        """:returns BinaryTree"""
        if self.key is None:  # Empty tree
            return None

        while self._right:
            self = self._right

        return self

    def min_node(self):
        """:returns BinaryTree"""
        if self is None or self.key is None:  # Empty tree
            return None

        while self._left:
            self = self._left

        return self

    """ PUBLIC """

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

    def isMirror(root1, root2):
        # If both trees are empty, then they are mirror images
        if root1 is None and root2 is None:
            return True

        if root1 is not None and root2 is not None:
            if root1.key == root2.key:
                return BinaryTree.isMirror(root1._left, root2._right) and BinaryTree.isMirror(
                    root1._right, root2._left
                )

        # If none of the above conditions is true then root1
        # and root2 are not mirror images
        return False

    def isSymmetric(self):
        # Check if tree is mirror of itself
        return BinaryTree.isMirror(self, self)


if __name__ == "__main__":
    a = BinaryTree()
    for _ in [5, 1, 9, 3, 6, 10, 7, 16, 8, 2]:
        a.insert(_)

    a.inorder()
    print()
    print(a.key)
    print(a.max_node())
    print(a.max_node())
    print(a.max_node().key)
    print(a.key)
    a.delete(6)
    print([v for v in a.inorder()])
