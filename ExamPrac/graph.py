"""
CSCI-603: Graphs
Author: Sean Strout @ RIT CS

An implementation of a graph data structure as an adjacency list.

Code taken from the online textbook and modified:

http://interactivepython.org/runestone/static/pythonds/Graphs/Implementation.html
"""

from vertex import Vertex


class Graph:
    """
    A graph implemented as an adjacency list of vertices.

    :slot: vertList (dict):  A dictionary that maps a vertex key to a Vertex
        object
    :slot: numVertices (int):  The total number of vertices in the graph

    Note that it is actually the vertices that keep track of their neighbors.
    By combining the Graph and Vertex data structures, the proper description
    of this implementation would be an 'adjacency list'.
    """

    __slots__ = 'vertList', 'numVertices'

    def __init__(self, dataFile=None):
        """
        Initialize the graph
        :param dataFile: a text file of 'name name dist' lines to create
                         a directed graph. If dataFile is None, create
                         an empty graph and use addVertex and add_edge
                         to fill it.
        :return: None
        """
        self.vertList = dict()
        self.numVertices = 0
        if dataFile is not None:
            with open(dataFile, "r") as graphData:
                for line in graphData.readlines():
                    v1Name, v2Name, weight = line.strip().split()
                    self.add_edge(v1Name, v2Name, float(weight))

    def addVertex(self, key):
        """
        Add a new vertex to the graph, or replace an existing one if the
        key is a duplicate.
        :param key: The identifier for the vertex (typically a string)
        :return: Vertex
        """
        if key not in self.vertList:
            self.numVertices += 1
        vtx = Vertex(key)
        self.verList[key] = vtx
        return vtx

    def getVertex(self, key):
        """
        Retrieve the vertex from the graph.
        :param key: The vertex identifier
        :return: The Vertex in this graph with the given key if it is present,
                 otherwise None
        """
        return self.vertList[key]

    def __contains__(self, key):
        """
        Returns whether the vertex labeled with the key is in the graph or not.
        This allows the user to do:

            key in graph

        :param key: The vertex label
        :return: True if the vertex is present, and False if not
        """
        return key in self.vertList

    def add_edge(self, src, dest, cost=0):
        """
        Add a new directed edge from a source to a destination of an edge cost.
        :param src: The source vertex key
        :param dest: The destination vertex key
        :param cost: The edge cost (defaults to 0)
        :return: None
        """
        if src not in self.vertList:
            self.numVertices += 1
            self.vertList[src] = Vertex(src)
        if dest not in self.vertList:
            self.numVertices += 1
            self.vertList[dest] = Vertex(dest)
        self.vertList[src].add_neighbor(self.vertList[dest], cost)

    def get_vertex_keys(self):
        """
        Return the collection of keys of the vertices in the graph.
        :return: A list of vertex identifiers
        """
        return self.vertList.keys()

    def __str__(self):
        return "Graph(" + str(self.numVertices) + "):" + \
               str(list(self.vertList.keys()))

    def __iter__(self):
        """
        Return an iterator over the vertices in the graph.  This allows the
        user to do:

            for vertex in graph:
                ...

        :return: A list iterator over Vertex objects
        """
        return iter(self.vertList.values())


def testGraph():
    """
    A test function for the Graph class.
    :return: None
    """
    STATES = {
        'CT': ('MA', 'RI'),
        'MA': ('CT', 'NH', 'RI', 'VT'),
        'ME': ('NH',),
        'NH': ('MA', 'ME', 'VT'),
        'RI': ('CT', 'MA'),
        'VT': ('MA', 'NH')
    }

    # add all the edges to the graph
    northeast = Graph()
    for state, neighbors in STATES.items():
        for neighbor in neighbors:
            # this automatically creates a new vertices if not already present
            northeast.add_edge(state, neighbor)

    # display the vertices, which will show the connected neighbors.
    # this will call the __iter__() method to get the Vertex objects.
    for state in northeast:
        print(state)

    print(northeast)
    print(northeast.get_vertex_keys())

    # check the __contains__() method
    print('MA in northeast (True)?', 'MA' in northeast)
    print('CA in northeast (False)?', 'CA' in northeast)

    # test getVertex()
    print('MA vertex:', northeast.getVertex('MA'))


def test_input():
    wny = Graph("Tests/wny.txt")

    for state in wny:
        print(state)

    print(wny)
    print(wny.get_vertex_keys())

    # check the __contains__() method
    print('rochester in western ny (True)?', 'rochester' in wny)
    print('albany in western ny (False)?', 'albany' in wny)

    # test getVertex()
    print('rochester vertex:', wny.getVertex('rochester'))

    # test edge weights (distances)
    roch = wny.getVertex('rochester')
    adjacent = roch.get_connections()
    for cityName in 'buffalo', 'geneva', 'binghamton':
        city = wny.getVertex(cityName)
        if city in adjacent:
            print('rochester is', roch.get_weight(city), 'miles from',
                  cityName)
        else:
            print('rochester is not connected to', cityName)


if __name__ == '__main__':
    testGraph()
    # test_input( )
