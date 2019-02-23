__author__ = 'BR'

"""
Author: BIKASH ROY (Username - br8376)

File name: RingStack.py
"""


from ring_buffer import RingBuffer


class RingStack:
    '''
    A ring buffer based stack implementation. Keeps the new data and drops the old to insert new data
    '''
    def __init__(self, capacity):
        # store as instance variable
        self._capacity = capacity
        # create list of size capacity
        self.RingBuffer = RingBuffer(self._capacity)
        # set other instance variable defaults
        self.top = -1
        self.size = 0

    def __str__(self):
        '''
             A toString equivalent of java, which returns the string representation of the class
        '''
        # pretty print
        result = 'RingStack'
        result += str(self.RingBuffer)
        return result

    def insert(self, val):
        '''
            Method to insert data into stack
        '''
        self.top += 1
        if self.top == self._capacity:
            self.top = 0
        self.RingBuffer.insert_keep_new(val)
        # update pointers during insert to keep only newest data
        if self.size < self._capacity:
            self.size += 1

    def remove(self):
        '''
           Method to remove data from stack
        '''
        # no op if empty
        if self.size is 0:
            return
        # update pointers
        self.RingBuffer.element[self.top].element = None
        self.top -= 1
        if self.top is -1:
            self.top = self._capacity - 1
        self.size -= 1

    def peek(self):
        '''
             Returns top element of the buffer
        '''
        if self.RingBuffer.element[self.top].element is None and self.size > 0:
            self.top = self._capacity - self.size
        return self.RingBuffer.element[self.top].element

    def capacity(self):
        '''
            Returns buffer size
        '''
        return self._capacity


def test():
    '''
           A test method for ring stack
    '''
    print('Creating empty ListStack named "a" of size 3')
    a = RingStack(3)
    print('Creating empty ListStack named "b" of size 2')
    b = RingStack(2)

    print('peek on a', a.peek(), 'currently contains', a)
    print('peek on b', a.peek(), 'currently contains', b)
    for val in range(1, 4):
        print('inserting', val, 'into both a and b')
        a.insert(val)
        # won't fit all
        b.insert(val)
        print('peek on a', a.peek(), 'currently contains', a)
        print('peek on b', a.peek(), 'currently contains', b)

    for i in range(1, 3):
        print('removing', a.peek(), 'from a')
        a.remove()
        print('peek on a', a.peek(), 'currently contains', a)
        print('removing', b.peek(), 'from b')
        b.remove()
        print('peek on b', a.peek(), 'currently contains', b)

    for val in range(1, 3):
        print('inserting', val, 'into both a and b')
        a.insert(val)
        b.insert(val)
        print('peek on a', a.peek(), 'currently contains', a)
        print('peek on b', a.peek(), 'currently contains', b)


if __name__ == '__main__':
    '''
     Driver main
    '''
    test()