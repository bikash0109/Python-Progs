from Node import Node


class LinkedList:
    __slots__ = "front"

    def __init__(self):
        self.front = None

    def append(self, value):
        node = self.front
        if node is None:
            self.front = Node(value)
        else:
            while node.link is not None:
                node = node.link
            node.link = Node(value)

    def prepend(self, value):
        self.front = Node(value, self.front)

    def start(self):
        return self.front

    def is_off(self, cursor):
        return cursor is None

    def get_value(self, cursor):
        if self.is_off(cursor):
            raise ValueError()
        return cursor.value

    def set_value(self, cursor, value):
        if self.is_off(cursor):
            raise ValueError()
        cursor.value = value

    def next_loc(self, cursor):
        if self.is_off(cursor):
            raise ValueError()
        return cursor.link

    def insert(self, cursor, value):
        if cursor is self.front:
            self.prepend(value)
        else:
            node = self.front
            while node.link is not cursor:
                node = node.link
            node.link = Node(value, cursor)

    def size(self):
        return self.size_to_end(self.front)

    def size_to_end(self, node):
        if node is None:
            return 0
        else:
            return 1 + self.size_to_end(node.link)

    class Iter:
        __slots__ = "cursor", "list"

        def __next__(self):
            if self.list.is_off(self.cursor):
                raise StopIteration()
            else:
                result = self.list.get_value(self.cursor)
                self.cursor = self.list.next_loc(self.cursor)
                return result

    def __iter__(self):
        result = LinkedList.Iter()
        result.list = self
        result.cursor = self.start()
        return result

    def iter2(self):
        cursor = self.start()
        while not self.is_off(cursor):
            yield self.get_value(cursor)
            cursor = self.next_loc(cursor)

    def iter3(self, action):
        cursor = self.start()
        while not self.is_off(cursor):
            action(self.get_value(cursor))
            cursor = self.next_loc(cursor)


def print_list(seq, msg):
    """ Print the contents of a list on a single line, first to last.
    """
    print("%s\n===============\n[%d] " % (msg, seq.size()), end="")
    cursor = seq.start()
    while not seq.is_off(cursor):
        print(seq.get_value(cursor), end=" ")
        cursor = seq.next_loc(cursor)
    print()

    print("%s\n===============\n[%d] " % (msg, seq.size()), end="")
    for element in seq:
        print(element, end=" ")
    print()

    print("%s\n===============\n[%d] " % (msg, seq.size()), end="")
    for element in seq.iter2():
        print(element, end=" ")
    print()

    print("%s\n===============\n[%d] " % (msg, seq.size()), end="")
    seq.iter3(lambda element: print(element, end=" "))
    print()


def test():
    # Create a list.
    seq = LinkedList()
    print_list(seq, "START")

    # Add values using append.
    for even in 4, 6:
        seq.append(even)

    # Prepend a value
    seq.prepend(2)
    print_list(seq, "EVENS")

    # Weave additional elements in to the list.
    odd = 1
    cursor = seq.start()
    while not seq.is_off(cursor):
        seq.insert(cursor, odd)
        odd += 2
        cursor = seq.next_loc(cursor)
    seq.insert(cursor, odd)

    print_list(seq, "UPTO7")

    # Test the set_value method.
    seq.set_value(seq.start(), -1)
    print_list(seq, "NEGTV")


if __name__ == "__main__":
    test()
