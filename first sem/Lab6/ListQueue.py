class ListQueue:
    '''
    This is a list based implementation of a queue which will keep oldest data
    and drop anything new that there is not room for
    '''
    def __init__(self, capacity):
        # create list of size capacity
        self.list_queue = [None] * capacity
        # store as instance variable
        self._capacity = capacity
        # set other instance variable defaults
        self.front = -1
        self.back = -1
        self.size = 0

    def __str__(self):
        # pretty print
        result = 'ListQueue['
        for val in self.list_queue:
            result += ' ' + str(val)
        return result + ']'

    def insert(self, val):
        # if at end of list, ignore add
        if self.back is self._capacity - 1:
            return
        # update pointers during insert to keeping only oldest data
        if self.front is -1:
            self.front = 0
        self.back += 1
        self.list_queue[self.back] = val
        self.size += 1

    def remove(self):
        # no op if empty
        if self.size is 0:
            return
        # update pointers
        self.list_queue = self.list_queue[1:] + [None]
        self.back -= 1
        if self.back is -1:
            self.front = -1
        self.size -= 1

    def peek(self):
        return self.list_queue[self.front]

    def capacity(self):
        return self._capacity


def test():
    print('Creating empty ListQueue named "a" of size 3')
    a = ListQueue(3)
    print('Creating empty ListQueue named "b" of size 2')
    b = ListQueue(2)

    print('peek on a', a.peek(), 'currently contains', a)
    print('peek on b', a.peek(), 'currently contains', b)
    for val in range(3):
        print('inserting', val, 'into both a and b')
        a.insert(val)
        # won't fit all
        b.insert(val)
        print('peek on a', a.peek(), 'currently contains', a)
        print('peek on b', a.peek(), 'currently contains', b)

    for i in range(2):
        print('removing', a.peek(), 'from a')
        a.remove()
        print('peek on a', a.peek(), 'currently contains', a)
        print('removing', b.peek(), 'from b')
        b.remove()
        print('peek on b', a.peek(), 'currently contains', b)

    for val in range(2):
        print('inserting', val, 'into both a and b')
        a.insert(val)
        b.insert(val)
        print('peek on a', a.peek(), 'currently contains', a)
        print('peek on b', a.peek(), 'currently contains', b)


if __name__ == '__main__':
    test()