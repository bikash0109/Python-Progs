"""
CSCI-603: Graphs
Author: Sean Strout @ RIT CS

An implementation of a vertex as part of a graph.

Code taken from the online textbook and modified:

http://interactivepython.org/runestone/static/pythonds/Graphs/Implementation.html
"""


class Vertex:
    """
    An individual vertex in the graph.

    :slots: key:  The identifier for this vertex (user defined, typically
        a string)
    :slots connected_to:  A dictionary of adjacent neighbors, where the key is
        the neighbor (Vertex), and the value is the edge cost (int)
    """

    __slots__ = "key", "connected_to"

    def __init__(self, key):
        """
        Initialize a vertex
        :param key: The identifier for this vertex
                    It is called a key because it is both a vertex id and
                    a key for the graph's dictionary of vertices.
        :return: None
        """
        self.key = key
        self.connected_to = dict()

    def add_neighbor(self, nbr, weight=0):
        """
        Connect this vertex to a neighbor with a given weight (default is 0).
        :param nbr (Vertex): The neighbor vertex
        :param weight (int): The edge weight (cost)
        :return: None
        """
        self.connected_to[nbr] = weight

    def __str__(self):
        """
        Return a string representation of the vertex and its direct neighbors:

            vertex-id->[neighbor-1-key, neighbor-2-key, ...]

        :return: The string
        """
        return str(self.key) + "->" + str(
            [str(x.key) for x in self.connected_to])

    def get_connections(self):
        """
        Get the neighbor vertices.
        :return: A list of Vertex neighbors
        """
        return self.connected_to.keys()

    def get_weight(self, nbr):
        """
        Get the edge cost to a neighbor.
        :param nbr (Vertex): The neighbor vertex
        :return: The weight (int)
        """
        return self.connected_to[nbr]

    def __eq__(self, other):
        """
        Two vertices are equal if they have the same key.
        (Neighbors may come and go.)
        :param other: the vertex to which this one is being compared
        :return: true iff both vertices have the same key.
        """
        return self.key == other.key

    def __ne__(self, other):
        """
        Two vertices are equal if they have the same key.
        (Neighbors may come and go.)
        :param other: the vertex to which this one is being compared
        :return: true iff both vertices have the same key.
        """
        return self.key != other.key

    def __hash__(self):
        """
        Since vertices are compared only by their keys, the hash code is
        only based on the key.
        :return: the hash of the vertex's key
        """
        return hash(self.key)


def test_vertex():
    """
    A test function for the Vertex class.
    :return: None
    """
    vertexA = Vertex('A')
    vertexB = Vertex('B')
    vertexC = Vertex('C')
    vertexD = Vertex('D')
    vertexA.add_neighbor(vertexB, 3)
    vertexA.add_neighbor(vertexC, 1)
    vertexB.add_neighbor(vertexA, 4)
    vertexB.add_neighbor(vertexC, 2)
    vertexC.add_neighbor(vertexD, 5)

    # test __str__()
    print(vertexA)
    print(vertexD)

    # test get_weight()
    print('A -> B weight (3):', vertexA.get_weight(vertexB))
    print('C -> D weight (5):', vertexC.get_weight(vertexD))

    # test get_connections():
    print("B's neighbors ():",
          [vertex.key for vertex in vertexB.get_connections()])
    print("D's neighbors ():", list(vertexD.get_connections()))


if __name__ == '__main__':
    test_vertex()
