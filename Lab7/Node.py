class Node:
    __slots__ = "value", "link"

    def __init__(self, value, link=None):
        self.value = value
        self.link = link

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Node(" + repr(self.value) + "," + repr(self.link) + ")"


def test():
    nodes = Node(1, Node(3, Node("Bikash")))
    n = nodes
    while n is not None:
        print(n)
        n = n.link
    print(nodes)
    print(repr(nodes))


if __name__ == "__main__":
    test()