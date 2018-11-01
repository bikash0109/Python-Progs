from enum import Enum


class NodeConstants(Enum):
    FRONT_NODE = 1


class Node:
    def __init__(self, element=None, next_node=None):
        self.element = element
        self.next_node = next_node

    def __str__(self):
        if self.element:
            return self.element.__str__()
        else:
            return 'Empty Node'

    def __repr__(self):
        return self.__str__()


class RingBuffer:
    def __init__(self):
        self.head = Node(element=NodeConstants.FRONT_NODE)
        self.head.next_node = self.head

    def size(self):
        count = 0
        current = self.head.next_node

        while current != self.head:
            count += 1
            current = current.next_node

        return count

    def insert_front(self, data):
        node = Node(element=data, next_node=self.head.next_node)
        self.head.next_node = node

    def insert_last(self, data):
        current_node = self.head.next_node

        while current_node.next_node != self.head:
            current_node = current_node.next_node

        node = Node(element=data, next_node=current_node.next_node)
        current_node.next_node = node

    def insert(self, data, position):
        if position == 0:
            self.insert_front(data)
        elif position == self.size():
            self.insert_last(data)
        else:
            if 0 < position < self.size():
                current_node = self.head.next_node
                current_pos = 0

                while current_pos < position - 1:
                    current_pos += 1
                    current_node = current_node.next_node

                node = Node(data, current_node.next_node)
                current_node.next_node = node
            else:
                raise IndexError

    def remove_first(self):
        self.head.next_node = self.head.next_node.next_node

    def remove_last(self):
        current_node = self.head.next_node

        while current_node.next_node.next_node != self.head:
            current_node = current_node.next_node

        current_node.next_node = self.head

    def remove(self, position):
        if position == 0:
            self.remove_first()
        elif position == self.size():
            self.remove_last()
        else:
            if 0 < position < self.size():
                current_node = self.head.next_node
                current_pos = 0

                while current_pos < position - 1:
                    current_node = current_node.next_node
                    current_pos += 1

                current_node.next_node = current_node.next_node.next_node
            else:
                raise IndexError

    def fetch(self, position):
        if 0 <= position < self.size():
            current_node = self.head.next_node
            current_pos = 0

            while current_pos < position:
                current_node = current_node.next_node
                current_pos += 1

            return current_node.element
        else:
            raise IndexError