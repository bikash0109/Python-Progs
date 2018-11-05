__author__ = 'BR'

"""
Author: BIKASH ROY (Username - br8376)

File name: router_test.py
"""

import unittest
from ring_buffer import RingBuffer
from stack import RingStack
from queue import RingQueue
from ListStack import ListStack
from ListQueue import ListQueue


class TestRingBufferDS(unittest.TestCase):
    '''
        A ring buffer test class
    '''
    names = ['Bob Belcher',
             'Linda Belcher',
             'Tina Belcher',
             'Gene Belcher',
             'Louise Belcher']

    def test_init(self):
        rb = RingBuffer(4)
        rs = RingStack(4)
        rq = RingQueue(4)
        ls = ListStack(4)
        lq = ListQueue(4)
        self.assertIsNotNone(rb.head)
        self.assertEqual(rb.size(), 0)
        self.assertEqual(rs.top, -1)
        self.assertEqual(rs.size, 0)
        self.assertEqual(ls.top, -1)
        self.assertEqual(ls.size, 0)
        self.assertEqual(rq.front, -1)
        self.assertEqual(rq.back, -1)
        self.assertEqual(rq.size, 0)
        self.assertEqual(lq.front, -1)
        self.assertEqual(lq.back, -1)
        self.assertEqual(lq.size, 0)

    def test_insert(self):
        rb = RingBuffer(4)
        rs = RingStack(4)
        rq = RingQueue(4)
        ls = ListStack(4)
        lq = ListQueue(4)
        for name in TestRingBufferDS.names:
            rb.insert_keep_old(name)
            rs.insert(name)
            rq.insert(name)
            ls.insert(name)
            lq.insert(name)

        print("RingBuffer:", rb)
        print("RingStack:", rs)
        print("RingQueue:", rq)
        print("ListStack:", ls)
        print("ListQueue:", lq)

    def test_remove(self):
        rb = RingBuffer(4)
        rs = RingStack(4)
        rq = RingQueue(4)
        ls = ListStack(4)
        lq = ListQueue(4)
        for name in TestRingBufferDS.names:
            rb.insert_keep_old(name)
            rs.insert(name)
            rq.insert(name)
            ls.insert(name)
            lq.insert(name)

        print("Before remove: ")
        print("RingBuffer:", rb)
        print("RingStack:", rs)
        print("RingQueue:", rq)
        print("ListStack:", ls)
        print("ListQueue:", lq)

        for i in range(2):
            rs.remove()
            rq.remove()
            ls.remove()
            lq.remove()

        print("After remove: ")
        print("RingBuffer:", rb)
        print("RingStack:", rs)
        print("RingQueue:", rq)
        print("ListStack:", ls)
        print("ListQueue:", lq)


if __name__ == '__main__':
    unittest.main()