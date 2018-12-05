"""
This class is a heap implementation
"""
__author__ = 'Bikash Roy - br8376', 'Tanay Bhardwaj'


class Heap(object):
    '''
    Heap that orders by a given comparison function, default to less-than.
    '''
    __slots__ = ('value', 'size', 'compare_value', 'keys', 'bucket')

    def __init__(self, compare_value=lambda x, y: x < y):
        '''
        Constructor takes a comparison function.
        :param compare_value: Function that takes in two keys and returns a boolean
        if the first arg goes higher in the heap than the second
        '''
        self.value = []
        self.size = 0
        self.compare_value = compare_value
        self.bucket = {}
        self.keys = []

    def __root(self, pos):
        '''
        Helper function to compute the parent location of an index
        :param pos: Index in the heap
        :return: Index of parent
        '''
        return (pos - 1) // 2

    def __shuffle_up(self, pos):
        '''
        :param pos: start position
        '''
        while pos > 0 and \
                self.compare_value(self.keys[pos], self.keys[self.__root(pos)]):
            self.__swap(pos, self.__root(pos))
            pos = self.__root(pos)

    def __swap(self, i, j):
        """
        Swap the items at position i and j, and their keys, and update bucket
        """
        self.value[i], self.value[j] = self.value[j], self.value[i]
        self.keys[i], self.keys[j] = self.keys[j], self.keys[i]
        self.bucket[self.value[i]] = i
        self.bucket[self.value[j]] = j

    def __shuffle_down(self, pos):
        '''
        :param pos: start position
        '''
        swap_pos = self.__smallest(pos)
        while swap_pos != pos:
            self.__swap(pos, swap_pos)
            pos = swap_pos
            swap_pos = self.__smallest(pos)

    def __smallest(self, pos):
        '''
        Finds the "smallest" value of position and position's two children.
        :param pos: Index
        :return: index of smallest value
        '''
        item1 = pos * 2 + 1
        item2 = pos * 2 + 2
        if item1 >= self.size:
            return pos
        if item2 >= self.size:
            if self.compare_value(self.keys[pos], self.keys[item1]):
                return pos
            else:
                return item1
        if self.compare_value(self.keys[item1], self.keys[item2]):
            if self.compare_value(self.keys[pos], self.keys[item1]):
                return pos
            else:
                return item1
        else:
            if self.compare_value(self.keys[pos], self.keys[item2]):
                return pos
            else:
                return item2

    def insert(self, item, key=None):
        '''
        Inserts an item into the heap.
        :param item: Item to be inserted
        :param key:  The key for the item.  Defaults to the item if not given.
        '''
        if key is None:
            key = item

        if self.size < len(self.value):
            self.value[self.size] = item
            self.keys[self.size] = key
        else:
            self.value.append(item)
            self.keys.append(key)
        self.size += 1
        self.bucket[item] = self.size - 1
        self.__shuffle_up(self.size - 1)

    def pop(self):
        '''
        Removes and returns top of the heap
        :return: Item on top of the heap
        '''
        retjob = self.value[0]
        self.size -= 1
        # if we are popping the only element, assignment will fail,
        # but bubbling is unnecessary, so:
        if self.size > 0:
            self.value[0] = self.value.pop(self.size)  # PYTHON LIST POP NOT HEAP POP
            self.keys[0] = self.keys.pop(self.size)
            self.__shuffle_down(0)
        return retjob

    def __len__(self):
        '''
        Defining the "length" of a value structure also allows it to be
        used as a boolean value!
        :return: size of heap
        '''
        return self.size


