import turtle

PROGNAME = 'Sierpinski Carpet'

myPen = turtle.Turtle()
myPen.speed(10)
myPen.color("#000000")


# This function draws a box by drawing each side of the square and using the fill function
def box(boxSize):
    myPen.begin_fill()
    # 0 deg.
    myPen.forward(boxSize)
    myPen.left(90)
    # 90 deg.
    myPen.forward(boxSize)
    myPen.left(90)
    # 180 deg.
    myPen.forward(boxSize)
    myPen.left(90)
    # 270 deg.
    myPen.forward(boxSize)
    myPen.end_fill()
    myPen.setheading(0)


# Position myPen in center of the screen
myPen.penup()
myPen.goto(-50, -50)
myPen.pendown()

# draw the first box
box(100)


alist = [[1], [2], [3], [4]]
print(alist[2][0])
