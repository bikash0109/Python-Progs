
class RingBuffer:
    def __init__(self, size):
        self.element = [None for i in range(size)]
        self.next_node = [None for i in range(size)]

    def append(self, x):
        self.element.pop(0)
        self.element.append(x)

    def __str__(self):
        if self.element:
            return self.element.__str__()
        else:
            return 'Empty Node'

    def __repr__(self):
        return self.__str__()


buf = RingBuffer(4)
for i in range(10):
    buf.append(i)
    print(buf.__repr__())

