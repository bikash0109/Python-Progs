'''
balances.py
This program creates a balance puzzle from an input file, solves any missing weights, and draws the balance puzzle using
the turtle.
'''

__author__ = 'Bikash Roy - br8376', 'Tanay Bhardwaj'

import turtle
import sys


class Beam:
    __slots__ = 'name', 'left', 'right', 'distance', 'branch', 'pixel', 'weight'

    def __init__(self, name):
        """
        It initializes the name of the beam, and the other values needed by the beam.
        :param name: the name of this beam
        :return: None
        """
        self.name = name
        self.branch = list()
        self.left = 0
        self.right = 0
        self.distance = 0
        self.pixel = 1
        self.weight = 0

    def insert(self, branch):
        """
        This method adds an object to the list of objects branching from this beam
        :param branch: an object branching from this beam
        :return: None
        """
        self.branch.append(branch)

    def scaleFactor(self):
        """
        This method determines scale factor that is, there are at least 20 pixels
        apart.
        :return: sum of the left extends and sum of the right extents
        """
        leftSum = 0
        rightSum = 0
        longestBeam = 0
        for index in range(len(self.branch) - 1):
            leftFirst, leftSecond = self.branch[index].scaleFactor()
            rightFirst, rightSecond = self.branch[index + 1].scaleFactor()
            if index == 0:
                leftSum = leftFirst
            elif index == len(self.branch) - 2:
                rightSum = rightSecond
            total = abs(leftSecond) + 20 + abs(rightFirst)
            totalPerTick = total / (abs((self.branch[index].distance * -1) + self.branch[index + 1].distance))
            if totalPerTick > longestBeam:
                longestBeam = totalPerTick
        self.pixel = longestBeam
        self.left = self.left * self.pixel
        self.right = self.right * self.pixel
        return self.left + leftSum, self.right + rightSum

    def balanceTree(self):
        """
        This method checks all weights in the balance puzzle. If it encounters a weight of negative one, it calculates
        the calcWeight weight to balance the puzzle and changes the negative weight to that value.
        :return: the weight of this object
        """
        totalWeight = 0
        leftTorque = 0
        rightTorgue = 0
        missingBalance = None
        missingWeight = 0
        for item in self.branch:
            weight = item.balanceTree()
            if weight < 0:
                missingBalance = item
            else:
                totalWeight = totalWeight + weight
                if item.distance < 0:
                    leftTorque = leftTorque + (weight * item.distance)
                else:
                    rightTorgue = rightTorgue + (weight * item.distance)
        if missingBalance is not None:
            missingWeight = abs((leftTorque + rightTorgue) / missingBalance.distance)
            missingBalance.weight = missingWeight
            print("Missing weight: ", missingBalance.weight)
        self.weight = totalWeight + missingWeight
        print("Beam weight: ", self.weight)
        return self.weight

    def draw(self):
        """
        This method draws the beam that it is called on and all weights branching from it.
        :return: None
        :pre: Pos ( 0, 0 ) Heading East
        :pre: Heading South
        :post: Heading South
        """
        turtle.setheading(270)
        turtle.forward(30)
        turtle.right(90)
        i = 0
        while i != len(self.branch) and int(self.branch[i].distance) < 0:
            turtle.forward((self.branch[i].distance * -1) * self.pixel)
            turtle.left(90)
            self.branch[i].draw()
            turtle.right(90)
            turtle.back((self.branch[i].distance * -1) * self.pixel)
            i = i + 1
        turtle.right(180)
        while i != len(self.branch) and int(self.branch[i].distance) > 0:
            turtle.forward(self.branch[i].distance * self.pixel)
            turtle.right(90)
            self.branch[i].draw()
            turtle.left(90)
            turtle.back(self.branch[i].distance * self.pixel)
            i = i + 1
        turtle.right(90)
        turtle.back(30)


class Weight:
    __slots__ = 'weight', 'distance'

    def __init__(self, distance, weight):
        """
        :param distance: the distance of this weight from the center of the beam
        :param weight: the weight of this weight
        :return: None
        """
        self.weight = weight
        self.distance = distance

    def scaleFactor(self):
        """
            This method returns 0, o. Same name as Beam Class to support recursive calls
            :return: the weight of this weight object
        """
        return 0, 0

    def balanceTree(self):
        """
        This method returns the weight of this weight object. Same name as Beam Class to support recursive calls
        :return: the weight of this weight object
        """
        return self.weight

    def draw(self):
        """
        This method draws the weight.
        :return: None
        :pre: Heading: South, Pos : Handing from Beam
        :post: Heading: South, Pos : Handing from Beam
        """
        turtle.forward(20)
        turtle.up()
        turtle.forward(10)
        turtle.down()
        turtle.write(str(self.weight))
        turtle.up()
        turtle.back(10)
        turtle.down()
        turtle.back(20)


def makeTree(fileName):
    """
    This function opens a balance puzzle file, creates the balance tree with missing objects if any.
    :param fileName: the name of the balance puzzle file
    :return: the 'root' beam of the balance puzzle
    """
    head = None
    beamList = list()
    with open(fileName) as file:
        for line in file:
            lineArray = line.split()
            beem = Beam(lineArray[0])
            if lineArray[0] == 'B':
                head = beem
            for i in range(1, len(lineArray), 2):
                if i == 1:
                    beem.left = int(lineArray[i])
                elif i == len(lineArray) - 2:
                    beem.right = int(lineArray[i])
                foundAnotherBeam = False
                for item in beamList:
                    if lineArray[i + 1] == item.name:
                        item.distance = int(lineArray[i])
                        beem.insert(item)
                        foundAnotherBeam = True
                if not foundAnotherBeam:
                    w = Weight(int(lineArray[i]), int(lineArray[i + 1]))
                    beem.insert(w)
            beamList.append(beem)
    return head


def main():
    """
    The main function.
    :return: None
    :pre: No pre conditions
    :post: Pos( 0, 0 ) Heading( east )
    """
    args = sys.argv
    if len(args) < 2:
        print("File name missing")
        return
    fileName = args[1]
    tree = makeTree(fileName)
    tree.scaleFactor()
    tree.balanceTree()
    turtle.screensize(800, 800)
    turtle.speed(0)
    tree.draw()
    turtle.mainloop()


if __name__ == '__main__':
    main()
