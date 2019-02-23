'''
escape_point.py
This program creates a graph from
pond_data files, solves the graph to find the shortest path to exit.
'''

__author__ = 'Bikash Roy - br8376', 'Tanay Bhardwaj'

import heap
import sys


class Point(object):
    """
    This class is used to represent a point in a frozen pond pond_maze in a graph representation of that pond_maze.
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
    This function builds a frozen pond_maze and prints
    the shortest paths for every point on the pond, if
    they exist.
    :param file_name: the name of the test file from
                         which the pond_maze shall be built
    :return: None
    """
    all_possible_paths = {}

    # Open the file
    with open(file_name) as file:
        # Get the lines of the file
        lines = file.readlines()
        numbers = lines[0].split()
        pond_height = int(numbers[0])
        pond_width = int(numbers[1])
        escape_point = int(numbers[2])
        pond_data = [[None for column in range(pond_width)] for row in range(pond_height)]
        for line in range(pond_height):
            pond_data[line] = list(lines[line + 1])

    pond_maze = [[None for column in range(pond_width + 1)] for row in range(pond_height)]
    for row in range(pond_height):
        for column in range(pond_width):
            if pond_data[row][column] == '.':
                position = Point(row, column)
                if column - 1 >= 0 and pond_data[row][column - 1] == '.':
                    position.left = pond_maze[row][column - 1]
                    if pond_maze[row][column - 1] is not None:
                        pond_maze[row][column - 1].right = position
                if column + 1 < pond_width and pond_data[row][column + 1] == '.':
                    position.right = pond_maze[row][column + 1]
                    if pond_maze[row][column + 1] is not None:
                        pond_maze[row][column + 1].left = position
                if row - 1 >= 0 and pond_data[row - 1][column] == '.':
                    position.up = pond_maze[row - 1][column]
                    if pond_maze[row - 1][column] is not None:
                        pond_maze[row - 1][column].down = position
                if row + 1 < pond_height and pond_data[row + 1][column] == '.':
                    position.down = pond_maze[row + 1][column]
                    if pond_maze[row + 1][column] is not None:
                        pond_maze[row + 1][column].up = position
                if column == pond_width - 1 and row == escape_point:
                    pond_maze[escape_point][column + 1] = Point(escape_point, column + 1)
                    position.right = pond_maze[escape_point][column + 1]
                pond_maze[row][column] = position

    for column in range(pond_width):
        for row in range(pond_height):
            if pond_maze[row][column] is not None:
                start_point = pond_maze[row][column]
                end_point = pond_maze[escape_point][pond_width]
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
    # Print
    if len(all_possible_paths) > 0:
        keys = list(all_possible_paths.keys())
        for i in keys:
            if i != 0:
                result = str(i) + ": " + str(all_possible_paths[i])
                print(result)
        result = "No path: " + str(all_possible_paths[keys[0]])
        print(result)
    else:
        print("No starting square.")


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
    cost = dict()
    cost[start_point] = 0
    visited = dict()
    visited[start_point] = None
    q = heap.Heap()
    q.insert(start_point, cost[start_point])

    while q:
        current = q.pop()
        steps = list()
        steps.append(slide(current, 'left'))
        steps.append(slide(current, 'up'))
        steps.append(slide(current, 'right'))
        steps.append(slide(current, 'down'))
        for n in steps:
            if n not in cost:
                cost[n] = cost[current] + 1
                visited[n] = current
                q.insert(n, cost[n])
    if end_point in cost:
        return retrace_old_path(start_point, end_point, visited)
    else:
        return None


def retrace_old_path(start, current, visited):
    """
    :param start:    Source node.
    :param current:  A traversing node.
    :param visited:     Dictionary from nodes to previous nodes.
    :return:         List of nodes.
    """
    if current != start:
        v = visited[current]
        return retrace_old_path(start, v, visited) + [current]
    else:
        return [start]


def main():
    """
    The main function.
    :return: None
    """
    first_test = 'test1.txt'
    print("\n" + "Test 1: ")
    find_path(first_test)

    second_test = 'test2.txt'
    print("\n" + "Test 2: ")
    find_path(second_test)

    third_test = 'test3.txt'
    print("\n" + "Test 3: ")
    find_path(third_test)

    sys.exit(0)


if __name__ == '__main__':
    main()
