__author__ = 'BR'

"""
Author: BIKASH ROY (Username - br8376)

File name: RingQueue.py
"""


from ring_buffer import RingBuffer


class RingQueue:
    '''
    A ring buffer implementation of queue, which keeps the old data the drops the new data to insert new data
    '''
    def __init__(self, capacity):
        # store as instance variable
        self._capacity = capacity
        # create list of size capacity
        self.RingBuffer = RingBuffer(self._capacity)
        # set other instance variable defaults
        self.front = -1
        self.back = -1
        self.size = 0

    def __str__(self):
        '''
        A toString equivalent of java, which returns the string representation of the class
        '''
        # pretty print
        result = 'RingQueue'
        result += str(self.RingBuffer)
        return result

    def insert(self, val):
        '''
        Method to insert data into queue
        '''
        # if at end of list, ignore add
        if self.back is self._capacity - 1:
            return
        # update pointers during insert to keeping only oldest data
        if self.front is -1:
            self.front = 0
        self.back += 1
        self.RingBuffer.insert_keep_old(val)
        self.size += 1

    def remove(self):
        '''
        Method to remove data from queue
        '''
        # no op if empty
        if self.size is 0:
            return
        # update pointers
        if self.size > 0:
            self.RingBuffer.element[self._capacity - self.size].element = None
        else:
            self.RingBuffer.element[self._capacity - 1].element = None
        self.back -= 1
        if self.back is -1:
            self.front = -1
        self.size -= 1

    def peek(self):
        '''
        Returns front element of the buffer
        '''
        return self.RingBuffer.element[self.front]

    def capacity(self):
        '''
        Returns buffer size
        '''
        return self._capacity


def test():
    '''
        A test method for ring queue
    '''
    print('Creating empty ListQueue named "a" of size 3')
    a = RingQueue(3)
    print('Creating empty ListQueue named "b" of size 2')
    b = RingQueue(2)

    print('peek on a', a.peek(), 'currently contains', a)
    print('peek on b', a.peek(), 'currently contains', b)
    for val in range(1, 4):
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