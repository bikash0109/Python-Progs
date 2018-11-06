import re
import sys

__author__ = 'zjb'
from collections import namedtuple

Entry = namedtuple('Entry', ('key', 'value'))

'''
To make sure that the DELETED sentinel does not match
anything we actually want to have in the table, make it
a unique (content-free!) object.
'''


class _delobj: pass


DELETED = Entry(_delobj(), None)


class Hashmap:
    __slots__ = 'table', 'numkeys', 'cap', 'maxload', 'collision', 'probesequence', 'hashfunction_number'

    def __init__(self, initsz=100, maxload=0.7, hashfunction_number=0):
        '''
        Creates an open-addressed hash map of given size and maximum load factor
        :param initsz: Initial size (default 100)
        :param maxload: Max load factor (default 0.7)
        '''
        self.cap = initsz
        self.table = [None for _ in range(self.cap)]
        self.numkeys = 0
        self.maxload = maxload
        self.collision = 0
        self.probesequence = []
        self.hashfunction_number = hashfunction_number

    def put(self, key, value):
        '''
        Adds the given (key,value) to the map, replacing entry with same key if present.
        :param key: Key of new entry
        :param value: Value of new entry
        '''
        probecount = 0
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index] != DELETED and self.table[index].key != key:
            self.collision += 1
            index += 1
            if index == len(self.table):
                index = 0
            probecount += 1
        if self.table[index] is None:
            self.numkeys += 1
            self.probesequence.append(key + "@" + str(probecount + 1))
        self.table[index] = Entry(key, value)
        if self.numkeys / self.cap > self.maxload:
            # rehashing
            self.probesequence = []
            oldtable = self.table
            # refresh the table
            self.cap *= 2
            self.table = [None for _ in range(self.cap)]
            self.numkeys = 0
            # put items in new table
            for entry in oldtable:
                if entry is not None and entry != DELETED:
                    self.put(entry.key, entry.value)

    def remove(self, key):
        '''
        Remove an item from the table
        :param key: Key of item to remove
        :return: Value of given key
        '''
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            index += 1
            if index == len(self.table):
                index = 0
        if self.table[index] is not None:
            self.table[index] = DELETED

    def get(self, key):
        '''
        Return the value associated with the given key
        :param key: Key to look up
        :return: Value (or KeyError if key not present)
        '''
        probecount = 0
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            index += 1
            if index == self.cap:
                index = 0
            probecount += 1
        if self.table[index] is not None:
            for idx, item in enumerate(self.probesequence):
                item = str(item).split("@")
                if item[0].strip() == key.strip():
                    self.probesequence[idx] = key + "@" + str(int(item[1].strip()) + probecount + 1)
            return str(self.table[index].value)
        else:
            raise KeyError('Key ' + str(key) + ' not present')

    def contains(self, key):
        '''
        Returns True/False whether key is present in map
        :param key: Key to look up
        :return: Whether key is present (boolean)
        '''
        probecount = 0
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            index += 1
            if index == self.cap:
                index = 0
        for idx, item in enumerate(self.probesequence):
            item = str(item).split("@")
            if item[0].strip() == key.strip():
                self.probesequence[idx] = key + "@" + str(int(item[1].strip()) + probecount + 1)
        return self.table[index] is not None

    def find_max(self):
        a = ""
        maximum = 0
        for i, value in enumerate(self.table):
            if value is not None and value is not Entry:
                if value[1] is not Entry:
                    if value[1] > maximum:
                        maximum = value[1]
                        a = value[0]
        return a

    def find_probe(self, max):
        for item in self.probesequence:
            if str(item).split("@")[0].strip() == max.strip():
                return str(item).replace("@", " - ")

    def hash_func(self, key):
        '''
        Not using Python's built in hash function here since we want to
        have repeatable testing...
        However it is terrible.
        Assumes keys have a len() though...
        :param key: Key to store
        :return: Hash value for that key
        '''
        # if we want to switch to Python's hash function, uncomment this:
        if self.hashfunction_number == 0:
            return hash(key)
        elif self.hashfunction_number == 1:
            return self.my_hash1(key)
        else:
            return self.my_hash2(key)

    def my_hash1(self, key):
        int_length = len(str(key)) // 4
        sum = 0
        for i in range(len(key)):
            c = key[i * 4:(i * 4) + 4]
            mult = 1
            for j in range(len(c)):
                sum += ord(c[j]) * mult
                mult *= 256
        c = key[0:int_length * 4]
        mult = 1
        for k in range(len(c)):
            sum += ord(c[k]) * mult
            mult *= 256
        return abs(sum) % self.cap

    def my_hash2(self, key):
        ch = list(key)
        sum = 0
        for i in range(len(key)):
            sum += ord(ch[i])
        return sum % self.cap


def printMap(map):
    for i in range(map.cap):
        print(str(i) + ": " + str(map.table[i]))


def testMap():
    map = Hashmap(initsz=5, hashfunction_number=1)
    with open("/usr/share/dict/words") as f:
        for line in f:
            for key in re.findall('\w+', line):
                key = str(key).lower().strip()
                print(key)
                if map.contains(key):
                    count = map.get(key)
                    map.put(key, int(count) + 1)
                else:
                    map.put(key, 1)
    max = map.find_max()
    print(map.contains(max))
    print(max + " : " + map.get(max))
    print("collision: ", map.collision)
    print("probe: ", map.find_probe(max))
    printMap(map)

    # map = Hashmap(initsz=5, hashfunction_number=1)
    # map.put('apple', 1)
    # map.put('banana', 2)
    # map.put('orange', 15)
    # printMap(map)
    # print(map.contains('apple'))
    # print(map.contains('grape'))
    # print(map.get('orange'))
    #
    # print('--------- adding one more to force table resize ')
    # map.put('grape', 7)
    # printMap(map)
    #
    # print('--------- testing remove')
    # map.remove('apple')
    # printMap(map)
    #
    # print('--------- testing add to a DELETED location')
    # map.put('peach', 16)
    # printMap(map)
    # print(map.get('grape'))


def main():
    map = Hashmap(initsz=5, hashfunction_number=1)
    with open("test.txt") as f:
        for line in f:
            for key in re.findall(r'\w+', line):
                key = str(key).lower().strip()
                if map.contains(key):
                    count = map.get(key)
                    map.put(key, int(count) + 1)
                else:
                    map.put(key, 1)
    max = map.find_max()
    print(map.contains(max))
    print(max + " : " + map.get(max))
    print("collision: ", map.collision)
    print("probe: ", map.find_probe(max))
    printMap(map)

    # testMap()


if __name__ == '__main__':
    main()
