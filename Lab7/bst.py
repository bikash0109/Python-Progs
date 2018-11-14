
from BTNode import BTNode


class BST:
    __slots__ = 'root', 'size'

    def __init__(self):
        self.root = None
        self.size = 0

    def __insert(self, val, node):
        if val < node.val:
            if node.left is None:
                node.left = BTNode(val)
            else:
                self.__insert(val, node.left)
        else:
            if node.right is None:
                node.right = BTNode(val)
            else:
                self.__insert(val, node.right)

    def insert(self, val):
        if self.root is None:
            self.root = BTNode(val)
        else:
            self.__insert(val, self.root)
        self.size += 1

    def __contains(self, val, node):
        if node is None:
            return False
        elif val == node.val:
            return True
        elif val < node.val:
            return self.__contains(val, node.left)
        else:
            return self.__contains(val, node.right)

    def contains(self, val):
        return self.__contains(val, self.root)

    def __height(self, node):
        if node is None:
            return -1
        else:
            return 1 + max(self.__height(node.left), self.__height(node.right))

    def height(self):
        return self.__height(self.root)

    def __inorder(self, node):
        if node is None:
            return ' '
        else:
            return self.__inorder(node.left) + \
                   str(node.val) + \
                   self.__inorder(node.right)

    def __str__(self):
        return self.__inorder(self.root)


def testBST():
    # a larger tree
    t3 = BST()
    for val in (17, 5, 35, 2, 16, 29, 38, 19, 33):
        t3.insert(val)
    print('t3:', t3)
    print('t3 size (9):', t3.size)
    print('t3 height (3)?', t3.height())


if __name__ == '__main__':
    testBST()