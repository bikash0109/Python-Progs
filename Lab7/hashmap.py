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


def find_probe(map, max):
    sumofprobes = 0
    for item in map.probesequence:
        sumofprobes += int(str(item).split("@")[1].strip())
    return sumofprobes

def printMap(map):
    for i in range(map.cap):
        print(str(i) + ": " + str(map.table[i]))


def testMap():
    output_list = "mango, mango, mango, mango, mango," \
                  "\norange, orange, orange, orange, orange, " \
                  "\nlol, lol,ki ki ki ki " \
                  "\nman man man man man"
    with open("hashtest.txt", "w") as output_file:
        output_file.write(str(output_list))
    # /usr/share/dict/words
    map = Hashmap(initsz=5, hashfunction_number=1)
    with open("hashtest.txt", encoding="utf8") as f:
        for line in f:
            for key in re.findall('\w+', line):
                key = str(key).lower().strip()
                if map.contains(key):
                    count = map.get(key)
                    map.put(key, int(count) + 1)
                else:
                    map.put(key, 1)
    max = map.find_max()
    print(max)
    print(map.contains(max))
    print(max + " : " + map.get(max))
    print("collision: ", map.collision)
    print("probe: ", find_probe(max))


def main():
    arguments = sys.argv
    if len(arguments) == 2:
        file_name = arguments[1]
        if ".txt" not in file_name:
            print("file extension missing")
            return
        map_python = Hashmap(initsz=5, hashfunction_number=0)
        map_my_hash1 = Hashmap(initsz=5, hashfunction_number=1)
        map_my_hash2 = Hashmap(initsz=5, hashfunction_number=2)
        with open(file_name, encoding="utf8") as f:
            for line in f:
                for key in re.findall(r'\w+', line):
                    key = str(key).lower().strip()
                    if map_python.contains(key):
                        count = map_python.get(key)
                        map_python.put(key, int(count) + 1)
                    else:
                        map_python.put(key, 1)
                    # for my_hash1
                    if map_my_hash1.contains(key):
                        count = map_my_hash1.get(key)
                        map_my_hash1.put(key, int(count) + 1)
                    else:
                        map_my_hash1.put(key, 1)
                    # for my_hash2
                    if map_my_hash2.contains(key):
                        count = map_my_hash2.get(key)
                        map_my_hash2.put(key, int(count) + 1)
                    else:
                        map_my_hash2.put(key, 1)

        print("Python Hash Function")
        max_python = map_python.find_max()
        print(max_python + " : " + map_python.get(max_python))
        print("collision: ", map_python.collision)
        print("probe: ", find_probe(map_python, max_python))
        # my_hash1
        print("**********************************************************************************")
        print("my_hash1 Hash Function")
        max_my_hash1 = map_python.find_max()
        print(max_my_hash1 + " : " + map_my_hash1.get(max_my_hash1))
        print("collision: ", map_my_hash1.collision)
        print("probe: ", find_probe(map_my_hash1, max_my_hash1))
        # my_hash2
        print("**********************************************************************************")
        print("my_hash2 Hash Function")
        max_my_hash2 = map_python.find_max()
        print(max_my_hash2 + " : " + map_my_hash2.get(max_my_hash2))
        print("collision: ", map_my_hash2.collision)
        print("probe: ", find_probe(map_my_hash2, max_my_hash2))
    else:
        print("Argument must contain only input txt file name.")


if __name__ == '__main__':
    main()
