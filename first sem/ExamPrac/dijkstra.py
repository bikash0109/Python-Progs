"""
Dijkstra class is simulation engine for building a graph
with weighted edges and running Dijkstra's algorithm to compute
the shortest path from a source node to a destination node.
"""

from graph import Graph
from vertex import Vertex

STOP = "!"


def main():
    filename = input("Enter graph data file name: ")

    g = Graph(filename)
    print("The graph is", g)

    start = input("\nstart node or '" + STOP + "' to quit: ")
    while start != STOP:

        if start not in g.get_vertex_keys():
            print(start, "is not a valid name of a node in the graph.")
        else:

            end = input("end node: ")
            if end not in g.get_vertex_keys():
                print(end, "is not a valid name of a node in the graph.")
            else:

                print("Determining shortest path...")

                path, distance = shortest_path(g, start, end)
                print("Path is", path)
                print("Distance:", distance)

        start = input("\nstart node or '" + STOP + "' to quit: ")


class DData:
    __slots__ = "vtx", "pred", "dist"

    def __init__(self, vertex, distance):
        self.vtx = vertex
        self.pred = None
        self.dist = distance

    def __str__(self):
        return "DData[" + str(self.vtx.key) + "<-" + \
               str(self.pred.vtx.key if self.pred else None) + "," + \
               str(self.dist) + "]"


class PrioQ:
    __slots__ = "values"  # dict: id -> instances of DData

    def __init__(self):
        self.values = dict()

    def is_empty(self):
        return len(self.values) == 0

    def insert(self, vertex: Vertex, distance=None):
        self.values[vertex.key] = DData(vertex, distance)

    def _top(self):
        assert not self.is_empty()
        minDist = None
        result = None
        for key in self.values:
            thisDist = self.values[key].dist
            if minDist is None or \
                    (thisDist is not None and thisDist < minDist):
                minDist = thisDist
                result = key
        assert result is not None
        return result

    def item(self):
        return self.values[self._top()]

    def remove(self):
        del self.values[self._top()]

    def get_ddata(self, key):
        return self.values.get(key, None)


def shortest_path(graph: Graph, startKey: str, endKey: str) \
        -> (list, float):
    """
    Compute the path through the graph from a start to a finish vertex
    whose sum of edge weights is minimized.
    :param graph: the graph in which to search
    :param startKey: the key name of the starting vertex
    :param endKey: the key name of the ending vertex
    :return: a tuple containing (1) a list of vertex names that form the
             path, in order from start to finish, and (2) the length
             (sum of edge weights) of that path.
             Or, if no path is found, ( [], -1 )
    """
    remaining = PrioQ()
    for v in graph:
        if v.key == startKey:
            remaining.insert(v, 0)
        else:
            remaining.insert(v)

    lowest = remaining.item()
    assert lowest.vtx.key == startKey

    while lowest.vtx.key != endKey:
        remaining.remove()
        if lowest.dist is None or remaining.is_empty():  # No way to get to end
            return [], -1
        thisDist = lowest.dist
        for u in lowest.vtx.get_connections():
            # Only do this if u is not final.
            u_ddata = remaining.get_ddata(u.key)
            if u_ddata is not None:
                newDist = thisDist + lowest.vtx.get_weight(u)
                if u_ddata.dist is None or newDist < u_ddata.dist:
                    u_ddata.dist = newDist
                    u_ddata.pred = lowest
        lowest = remaining.item()
    path = []
    if lowest.dist is None:  # We found the end, but it never got connected.
        totalDistance = -1
    else:
        totalDistance = lowest.dist
        ddata = lowest
        while ddata is not None:
            path.insert(0, ddata.vtx.key)
            ddata = ddata.pred

    return path, totalDistance


if __name__ == "__main__":
    main()
