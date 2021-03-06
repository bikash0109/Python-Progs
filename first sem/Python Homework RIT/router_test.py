
import unittest
from random import randint

class TestCircularLinkedList(unittest.TestCase):
    names = ['Bob Belcher',
             'Linda Belcher',
             'Tina Belcher',
             'Gene Belcher',
             'Louise Belcher']

    def test_init(self):
        dll = RingBuffer()
        self.assertIsNotNone(dll.head)
        self.assertEqual(dll.size(), 0)

    def test_insert_front(self):
        dll = RingBuffer()
        for name in TestCircularLinkedList.names:
            dll.insert_front(name)

        self.assertEqual(dll.fetch(0), TestCircularLinkedList.names[4])
        self.assertEqual(dll.fetch(1), TestCircularLinkedList.names[3])
        self.assertEqual(dll.fetch(2), TestCircularLinkedList.names[2])
        self.assertEqual(dll.fetch(3), TestCircularLinkedList.names[1])
        self.assertEqual(dll.fetch(4), TestCircularLinkedList.names[0])

    def test_insert_last(self):
        dll = RingBuffer()
        for name in TestCircularLinkedList.names:
            dll.insert_last(name)

        for i in range(len(TestCircularLinkedList.names) - 1):
            self.assertEqual(dll.fetch(i), TestCircularLinkedList.names[i])

    def test_insert(self):
        dll = RingBuffer()
        for name in TestCircularLinkedList.names:
            dll.insert_last(name)

        pos = randint(0, len(TestCircularLinkedList.names) - 1)

        dll.insert('Teddy', pos)
        self.assertEqual(dll.fetch(pos), 'Teddy')

    def test_remove_first(self):
        dll = RingBuffer()
        for name in TestCircularLinkedList.names:
            dll.insert_last(name)

        for i in range(dll.size(), 0, -1):
            self.assertEqual(dll.size(), i)
            dll.remove_first()

    def test_remove_last(self):
        dll = RingBuffer()
        for name in TestCircularLinkedList.names:
            dll.insert_last(name)

        for i in range(dll.size(), 0, -1):
            self.assertEqual(dll.size(), i)
            dll.remove_last()

    def test_remove(self):
        dll = RingBuffer()
        for name in TestCircularLinkedList.names:
            dll.insert_last(name)

        dll.remove(1)

        self.assertEqual(dll.fetch(0), 'Bob Belcher')
        self.assertEqual(dll.fetch(1), 'Tina Belcher')
        self.assertEqual(dll.fetch(2), 'Gene Belcher')
        self.assertEqual(dll.fetch(3), 'Louise Belcher')


if __name__ == '__main__':
    unittest.main()