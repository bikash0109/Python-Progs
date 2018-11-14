from Node import Node


class Stack:
    __slots__ = "top"

    def __init__(self):
        self.top = None

    def __str__(self):
        n = self.top
        result = "Stack[ "
        while n is not None:
            result += str(n.value) + " "
            n = n.link
        result += "]"
        return result

    def is_empty(self):
        return self.top is None

    def push(self, value):
        self.top = Node(value, self.top)

    def pop(self):
        self.top = self.top.link

    def peek(self):
        assert not self.is_empty(), "Stack is empty"
        return self.top.value

    insert = push
    remove = pop


def test():
    s = Stack()
    print(s)
    for value in 1, 2, 3:
        s.push(value)
        print(s)
    print("Popping:", s.peek())
    s.pop()
    print(s)
    for value in 15, 16:
        s.insert(value)
        print(s)
    print("Removing:", s.peek())
    s.remove()
    print(s)
    while not s.is_empty():
        print("Popping:", s.peek())
        s.pop()
        print(s)
    print("Trying one too many pops... ", end="")
    try:
        s.pop()
        print("Problem: it succeeded!")
    except Exception as e:
        print("Exception was '" + str(e) + "'")


if __name__ == "__main__":
    test()
