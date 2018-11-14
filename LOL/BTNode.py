
class BTNode:
    __slots__ = 'val', 'left', 'right'

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def testBTNode():
    left = BTNode(10)
    right = BTNode(20)
    parent = BTNode(30)
    parent.left = left
    parent.right = right
    print('parent (30):', parent.val)
    print('left (10):', parent.left.val)
    print('right (20):', parent.right.val)


if __name__ == '__main__':
    testBTNode()