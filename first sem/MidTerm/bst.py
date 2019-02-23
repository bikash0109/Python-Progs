from btnode import BTNode


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

    def __get_value(self, val, node):
        if node is None:
            return ""
        elif val == node.val:
            return val
        elif val < node.val:
            return self.__get_value(val, node.left)
        else:
            return self.__get_value(val, node.right)

    def print_last_three_added_order(self, list):
        rValue = " "
        for val in list:
            rValue += str(self.__get_value(val, self.root)) + " "
        print("last_three_added_order:", rValue.strip())

    def __inorder(self, node):
        if node is None:
            return ' '
        else:
            return self.__inorder(node.left) + \
                   str(node.val) + \
                   self.__inorder(node.right)

    def start(self):
        return self.root

    def get_third_cursor(self):
        node = self.root
        for i in range(3):
            node = node.right
        return node


    def print_last_three_value_order(self):
        if self.root.left is not None:
            rValue = str(self.root.val)
            rValue += str(self.__inorder(self.root.right)) + " "
            print("last_three_value_order:", rValue.strip())
        else:
            rValue = str(self.__inorder(self.get_third_cursor())) + " "
            print("last_three_value_order:", rValue.strip())

    def __str__(self):
        return self.__inorder(self.root)


def main():
    bst = BST()
    to_add = [5, 3, 6, 2, 7, 1]
    for val in to_add:
        bst.insert(val)
    print("list inserted into binary search tree:", to_add)
    print(bst)
    bst.print_last_three_added_order(to_add[-3:])
    bst.print_last_three_value_order()


if __name__ == '__main__':
    main()