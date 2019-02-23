class ListStack:
    '''
    This is a list based implementation of a stack which will keep newest data
    and drop anything oldest that there is not room for
    '''
    def __init__(self, capacity):
        # create list of size capacity
        self.list_stack = [None] * capacity
        # store as instance variable
        self._capacity = capacity
        # set other instance variable defaults
        self.top = -1
        self.size = 0

    def __str__(self):
        # pretty print
        result = 'ListStack['
        for val in self.list_stack[self.top::-1]:
            result += ' ' + str(val)
        for val in self.list_stack[-1:self.top:-1]:
            result += ' ' + str(val)
        return result + ']'

    def insert(self, val):
        # update pointers during insert to keep only newest data
        self.top += 1
        if self.top == self._capacity:
            self.top = 0
        self.list_stack[self.top] = val
        if self.size < self._capacity:
            self.size += 1

    def remove(self):
        # no op if empty
        if self.size is 0:
            return
        # update pointers
        self.list_stack[self.top] = None
        self.top -= 1
        if self.top is -1:
            self.top = self._capacity - 1
        self.size -=1

    def peek(self):
        return self.list_stack[self.top]

    def capacity(self):
        return self._capacity

def test():
    print('Creating empty ListStack named "a" of size 3')
    a = ListStack(3)
    print('Creating empty ListStack named "b" of size 2')
    b = ListStack(2)

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