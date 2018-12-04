"""
This class is a heap implementation
"""
__author__ = 'Bikash Roy - br8376', 'Tanay Bhardwaj'


class Heap(object):
    '''
    Heap that orders by a given comparison function, default to less-than.
    '''
    __slots__ = ('data', 'size', 'lessfn', 'keys', 'itemIndex')

    def __init__(self, lessfn=lambda x, y: x < y):
        '''
        Constructor takes a comparison function.
        :param lessfn: Function that takes in two keys and returns a boolean
        if the first arg goes higher in the heap than the second
        '''
        self.data = []  # the array
        self.size = 0  # the number of things in the heap
        self.lessfn = lessfn  # the comparison function
        self.itemIndex = {}  # hashmap from items to slots
        self.keys = []  # parallel array for keys in data

    def __parent(self, loc):
        '''
        Helper function to compute the parent location of an index
        :param loc: Index in the heap
        :return: Index of parent
        '''
        return (loc - 1) // 2

    def __bubbleUp(self, loc):
        '''
        Starts from the given location and moves the item at that spot
        as far up the heap as necessary
        :param loc: Place to start bubbling from
        '''
        while loc > 0 and \
                self.lessfn(self.keys[loc], self.keys[self.__parent(loc)]):
            self.__swap(loc, self.__parent(loc))
            loc = self.__parent(loc)

    def __swap(self, i, j):
        """
        Swap the items at position i and j, and their keys, and update itemIndex
        """
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.keys[i], self.keys[j] = self.keys[j], self.keys[i]
        self.itemIndex[self.data[i]] = i
        self.itemIndex[self.data[j]] = j

    def __bubbleDown(self, loc):
        '''
        Starts from the given location and moves the item at that spot
        as far down the heap as necessary
        :param loc: Place to start bubbling from
        '''
        swapLoc = self.__smallest(loc)
        while swapLoc != loc:
            self.__swap(loc, swapLoc)
            loc = swapLoc
            swapLoc = self.__smallest(loc)

    def __smallest(self, loc):
        '''
        Finds the "smallest" value of loc and loc's two children.
        Correctly handles end-of-heap issues.
        :param loc: Index
        :return: index of smallest value
        '''
        ch1 = loc * 2 + 1
        ch2 = loc * 2 + 2
        if ch1 >= self.size:
            return loc
        if ch2 >= self.size:
            if self.lessfn(self.keys[loc], self.keys[ch1]):
                return loc
            else:
                return ch1
        # now consider all 3
        if self.lessfn(self.keys[ch1], self.keys[ch2]):
            if self.lessfn(self.keys[loc], self.keys[ch1]):
                return loc
            else:
                return ch1
        else:
            if self.lessfn(self.keys[loc], self.keys[ch2]):
                return loc
            else:
                return ch2

    def decreaseKey(self, item, newkey):
        """
        Assumes item in heap!  Will break if not!
        Note that this assumes that the newKey will cause the
        item to bubble UP not down.
        :param item:  item in heap to have it's key decreased
        :param newKey:  the new value of the key.
        """
        idx = self.itemIndex[item]
        self.keys[idx] = newkey
        self.__bubbleUp(idx)

    def insert(self, item, key=None):
        '''
        Inserts an item into the heap.
        :param item: Item to be inserted
        :param key:  The key for the item.  Defaults to the item if not given.
        '''
        if key is None:
            key = item

        if self.size < len(self.data):
            self.data[self.size] = item
            self.keys[self.size] = key
        else:
            self.data.append(item)
            self.keys.append(key)
        self.size += 1
        self.itemIndex[item] = self.size - 1
        self.__bubbleUp(self.size - 1)

    def pop(self):
        '''
        Removes and returns top of the heap
        :return: Item on top of the heap
        '''
        retjob = self.data[0]
        self.size -= 1
        # if we are popping the only element, assignment will fail,
        # but bubbling is unnecessary, so:
        if self.size > 0:
            self.data[0] = self.data.pop(self.size)  # PYTHON LIST POP NOT HEAP POP
            self.keys[0] = self.keys.pop(self.size)
            self.__bubbleDown(0)
        return retjob

    def __len__(self):
        '''
        Defining the "length" of a data structure also allows it to be
        used as a boolean value!
        :return: size of heap
        '''
        return self.size


