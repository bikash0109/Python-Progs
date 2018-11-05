__author__ = 'BR'

"""
Author: BIKASH ROY (Username - br8376)

File name: ring_buffer.py
"""


class Node:
    '''
        A node class to achieve linked structure in ring buffer
    '''
    def __init__(self, element, next_node=None):
        self.element = element
        self.next_node = next_node

    def __str__(self):
        if self.element:
            return self.element.__str__()
        else:
            return 'None'

    def __repr__(self):
        return self.__str__()


class RingBuffer:
    '''
        A ring buffer, where last is pointing to first element in a list
    '''
    def __init__(self, capacity):
        '''
            Constructor -
            :parameter: capacity - max buffer size
        '''
        self._capacity = capacity
        self.element = [Node(None) for i in range(self._capacity)]
        self.head = self.element[0]
        self.tail = self.element[self._capacity - 1]
        self.tail.next_node = self.head
        self._size = 0

    def __str__(self):
        '''
              A toString equivalent of java, which returns the string representation of the class
        '''
        if self.element:
            return self.element.__str__()
        else:
            return 'None'

    def get_head(self):
        '''
            Returns the start of the buffer
        '''
        return self.element[0]

    def get_tail(self):
        '''
            Returns end of the buffer
        '''
        self.element[self._capacity - 1].next_node = self.get_head()
        return self.element[self.capacity() - 1]

    def capacity(self):
        '''
            Returns maximum buffer size
        '''
        return self._capacity

    def size(self):
        '''
            Returns size of the buffer
        '''
        return self._size

    def remove_oldest(self):
        '''
            Remove the oldest data from the buffer
        '''
        self.element.pop(0)

    def remove_newest(self):
        '''
            Remove the newest data from the buffer
        '''
        self.element.pop(self._capacity - 1)

    def insert_keep_new(self, x):
        '''
            A special insert, where recent data is kept, and oldest data a dropped
        '''
        new_node = Node(x, Node(self.get_head()))
        self.element[self._capacity - 1].next_node = new_node
        self.remove_oldest()
        self.element.append(new_node)
        if self.size() < self.capacity():
            self._size += 1

    def insert_keep_old(self, x):
        '''
           A special insert, where recent data is dropped, and oldest data a kept
        '''
        new_node = Node(x, Node(self.get_head()))
        if self.element[0].element is None:
            self.element[self._capacity - 1].next_node = new_node
            self.remove_oldest()
            self.element.append(new_node)
            if self.size() < self.capacity():
                self._size += 1
        else:
            self.element[self._capacity - 2].next_node = new_node
            self.remove_newest()
            self.element.append(new_node)

    def find(self, d):
        '''
           Find the passed value and returns the cursor
        '''
        counter = 0
        value_found = False
        this_node = self.get_tail()
        while counter < self.capacity():
            if this_node.element == d:
                value_found = True
                return this_node
            this_node = this_node.next_node
            counter += 1
        if value_found is False:
            return value_found

    def replace(self, cursor, value):
        '''
           Replaces a value in a given position
        '''
        if cursor > self._capacity or cursor < 0 :
            print("Index not found")
        self.element[cursor].element = value


def test():
    '''
       A test method for ring buffer
    '''
    a = RingBuffer(3)
    b = RingBuffer(3)

    print('RingBuffer on a', a)
    print('RingBuffer on b', b)
    for val in range(1, 4):
        a.insert_keep_new(val)
        print("\na")
        print(a)
        # won't fit all
        b.insert_keep_old(val)
        print("\nb")
        print(b)


if __name__ == '__main__':
    '''
         Driver main
    '''
    test()