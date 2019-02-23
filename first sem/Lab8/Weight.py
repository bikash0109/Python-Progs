import turtle

class Weight:

    __slots__ = 'weight', 'distance', 'left', 'right', 'scale'

    def __init__(self, distance, weight ):
        self.weight = weight
        self.distance = distance
        self.left = 0
        self.right = 0
        self.scale = 0

    def scaleFactor(self):
        return self.left, self.right

    def solveWeights(self):
        return self.weight

    def draw(self):
        turtle.forward(20)
        turtle.up()
        turtle.forward(10)
        turtle.down()
        turtle.write(str(self.weight), align = 'center')
        turtle.up()
        turtle.back(10)
        turtle.down()
        turtle.back(20)