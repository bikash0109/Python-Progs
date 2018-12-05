'''
escape.py
This program creates a graph from
text files, solves the graph to find the shortest path to exit.
'''

__author__ = 'Bikash Roy - br8376', 'Tanay Bhardwaj'

import heap
import sys


class Point(object):
    """
    This class is used to represent a point in a frozen pond puzzle in a graph representation of that puzzle.
    """
    __slots__ = 'row', 'column', 'left', 'right', 'up', 'down'

    def __init__(self, row=0, column=0, left=None, right=None, up=None, down=None):
        """
        :param row: The row value of this position
        :param column: The column value of this position
        :param left: The node representing the position to the left
        :param right: The node representing the position to the right
        :param up: The node representing the position above
        :param down: The node representing the position below
        :return: None
        """
        self.row = row
        self.column = column
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def __str__(self):
        """
        This method returns a string representation of points of the pond.
        :return: A string representation of this node.
        """
        return "(" + str(self.column) + ", " + str(self.row) + ")"


def find_path(file_name):
    """
    This function builds a frozen pond puzzle and finds
    the shortest paths for every point on the pond, if
    they exist.
    :param file_name: the name of the test file from
                         which the puzzle shall be built
    :return: A dictionary containing the points on the
             frozen pond for which there is a path to
             the exit, and a special list for points
             with no path
    """
    all_possible_paths = {}

    # Open the file
    with open(file_name) as file:
        # Get the lines of the file
        lines = file.readlines()

        numbers = lines[0].split()
        height = int(numbers[0])
        width = int(numbers[1])
        escape = int(numbers[2])

        text = [[' ' for column in range(width)] for row in range(height)]
        for line in range(height):
            text[line] = list(lines[line + 1])

    puzzle = pond_graph(text, width, height, escape)

    for column in range(width):
        for row in range(height):
            if puzzle[row][column] is not None:
                start_point = puzzle[row][column]
                end_point = puzzle[escape][width]
                path = find_shortest_path(start_point, end_point)
                if path is not None:
                    if all_possible_paths.get(len(path) - 1) is not None:
                        all_possible_paths[len(path) - 1].append("(" + str(column) + ", " + str(row) + ")")
                    else:
                        all_possible_paths[len(path) - 1] = list()
                        all_possible_paths[len(path) - 1].append("(" + str(column) + ", " + str(row) + ")")
                else:
                    if all_possible_paths.get(0) is not None:
                        all_possible_paths[0].append("(" + str(column) + ", " + str(row) + ")")
                    else:
                        all_possible_paths[0] = list()
                        all_possible_paths[0].append("(" + str(column) + ", " + str(row) + ")")
    return all_possible_paths


def pond_graph(pond_attribute, pond_width, pond_height, exit_path):
    """
    This function builds a 2d array of Point to make the graph of pond
    :param pond_attribute: the text representing the puzzle as
                       a 2d array of strings
    :param: pond_width
    :param: pond_height
    :param: exit_path
    :return: the 2d array of nodes that represents the puzzle
    """
    puzzle = [[None for column in range(pond_width + 1)] for row in range(pond_height)]
    for row in range(pond_height):
        for column in range(pond_width):
            if pond_attribute[row][column] == '.':
                position = Point(row, column)
                if column - 1 >= 0 and pond_attribute[row][column - 1] == '.':
                    position.left = puzzle[row][column - 1]
                    if puzzle[row][column - 1] is not None:
                        puzzle[row][column - 1].right = position
                if column + 1 < pond_width and pond_attribute[row][column + 1] == '.':
                    position.right = puzzle[row][column + 1]
                    if puzzle[row][column + 1] is not None:
                        puzzle[row][column + 1].left = position
                if row - 1 >= 0 and pond_attribute[row - 1][column] == '.':
                    position.up = puzzle[row - 1][column]
                    if puzzle[row - 1][column] is not None:
                        puzzle[row - 1][column].down = position
                if row + 1 < pond_height and pond_attribute[row + 1][column] == '.':
                    position.down = puzzle[row + 1][column]
                    if puzzle[row + 1][column] is not None:
                        puzzle[row + 1][column].up = position
                if column == pond_width - 1 and row == exit_path:
                    puzzle[exit_path][column + 1] = Point(exit_path, column + 1)
                    position.right = puzzle[exit_path][column + 1]
                puzzle[row][column] = position
    return puzzle


def slide(start, direction):
    """
    Keep sliding along a frozen pond from a starting position until hitting
    a rock or the edge of the pond.
    :param start: The starting position
    :param direction: The direction in which we are sliding
    :return: The position where we stop sliding
    """
    current = start
    if direction == 'left':
        while current.left is not None:
            current = current.left
    if direction == 'right':
        while current.right is not None:
            current = current.right
    if direction == 'up':
        while current.up is not None:
            current = current.up
    if direction == 'down':
        while current.down is not None:
            current = current.down
    return current


def find_shortest_path(start_point, end_point):
    """
    An implementation of Djikstra's algorithm for computing
    shortest paths.
    :param start_point:  the source node object
    :param end_point:    the destination node object
    :return:            List of node objects corresponding to the
                       shortest weighted path if a path exists.  Otherwise,
                       returns None.
    """

    dist = {}
    dist[start_point] = 0
    prev = {}
    prev[start_point] = None
    q = heap.Heap()
    q.insert(start_point, dist[start_point])

    while q:
        current = q.pop()
        stops = list()
        stops.append(slide(current, 'left'))
        stops.append(slide(current, 'up'))
        stops.append(slide(current, 'right'))
        stops.append(slide(current, 'down'))
        for n in stops:
            if n not in dist:
                dist[n] = dist[current] + 1
                prev[n] = current
                q.insert(n, dist[n])
    if end_point in dist:
        return retrace_old_path(start_point, end_point, prev)
    else:
        return None


def retrace_old_path(start, current, prev):
    """
    :param start:    Source node.
    :param current:  A traversing node.
    :param prev:     Dictionary from nodes to previous nodes.
    :return:         List of nodes.
    """
    if current != start:
        v = prev[current]
        return retrace_old_path(start, v, prev) + [current]
    else:
        return [start]


def output(paths):
    """
    This function prints out the results.
    :param: paths
    :return: None
    """
    if len(paths) > 0:
        keys = list(paths.keys())
        for i in keys:
            if i != 0:
                result = str(i) + ": " + str(paths[i])
                print(result)
        result = "No path: " + str(paths[keys[0]])
        print(result)
    else:
        print("No starting square.")


def main():
    """
    The main function.
    :return: None
    """
    first_test = 'test1.txt'
    print("\n" + "Test 1: ")
    output(find_path(first_test))

    second_test = 'test2.txt'
    print("\n" + "Test 2: ")
    output(find_path(second_test))

    third_test = 'test3.txt'
    print("\n" + "Test 3: ")
    output(find_path(third_test))

    sys.exit(0)


if __name__ == '__main__':
    main()
