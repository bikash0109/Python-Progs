class BTNode:

    __slots__ = 'val', 'left', 'right'

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
