from BTNode import BTNode


def preorder(node):
    if node is not None:
        print(node.val, end=' ')
        preorder(node.left)
        preorder(node.right)


def inorder(node):
    if node is not None:
        inorder(node.left)
        print(node.val, end=' ')
        inorder(node.right)


def postorder(node):
    if node is not None:
        postorder(node.left)
        postorder(node.right)
        print(node.val, end=' ')


def traverse(node):
    print('Traversing...')
    print('preorder:', end= ' ')
    preorder(node)
    print()
    print('inorder:', end= ' ')
    inorder(node)
    print()
    print('postorder:', end= ' ')
    postorder(node)
    print()


def testTraversals():
    # single node
    traverse(BTNode(10))

    # A parent node (20), with left (10) and right (30) children
    traverse(BTNode(20, BTNode(10), BTNode(30)))

    # from lecture notes: tree.png
    traverse(BTNode('A',
            BTNode('B',
                   None,
                   BTNode('D')),
            BTNode('C',
                   BTNode('E',
                          BTNode('G'),
                          None),
                   BTNode('F',
                          BTNode('H'),
                          BTNode('I')))))


if __name__ == '__main__':
    testTraversals()