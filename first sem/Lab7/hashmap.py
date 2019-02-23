from collections import namedtuple

Entry = namedtuple('Entry', ('key', 'value'))


class _delobj: pass


DELETED = Entry(_delobj(), None)


class Hashmap:

    __slots__ = 'table', 'numkeys', 'cap', 'maxload'

    def __init__(self, initsz=100, maxload=0.7):
        self.cap = initsz
        self.table = [None for _ in range(self.cap)]
        self.numkeys = 0
        self.maxload = maxload

    def put(self, key, value):
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and \
                        self.table[index] != DELETED and \
                        self.table[index].key != key:
            index += 1
            if index == len(self.table):
                index = 0
        if self.table[index] is None:
            self.numkeys += 1
        self.table[index] = Entry(key, value)
        if self.numkeys/self.cap > self.maxload:
            # rehashing
            oldtable = self.table
            # refresh the table
            self.cap *= 2
            self.table = [None for _ in range(self.cap)]
            self.numkeys = 0
            # put items in new table
            for entry in oldtable:
                if entry is not None:
                    self.put(entry[0],entry[1])

    def remove(self, key):
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            index += 1
            if index == len(self.table):
                index = 0
        if self.table[index] is not None:
            self.table[index] = DELETED

    def get(self,key):
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            index += 1
            if index == self.cap:
                index = 0
        if self.table[index] is not None:
            return self.table[index].value
        else:
            raise KeyError('Key ' + str(key) + ' not present')

    def contains(self, key):
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            index += 1
            if index == self.cap:
                index = 0
        return self.table[index] is not None

    def hash_func(self, key):
        # if we want to switch to Python's hash function, uncomment this:
        #return hash(key)
        return len(key)


def printMap(map):
    for i in range(map.cap):
        print(str(i)+": " + str(map.table[i]))


def testMap():
    map = Hashmap(initsz=5)
    map.put('apple',1)
    map.put('banana',2)
    map.put('orange',15)
    printMap(map)
    print(map.contains('apple'))
    print(map.contains('grape'))
    print(map.get('orange'))

    print('--------- adding one more to force table resize ')
    map.put('grape',7)
    printMap(map)

    print('--------- testing remove')
    map.remove('apple')
    printMap(map)

    print('--------- testing add to a DELETED location')
    map.put('peach', 16)
    printMap(map)
    print(map.get('grape'))


if __name__ == '__main__':
    testMap()