import turtle
import sys

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1400
SIDE_LENGTH = 200


def init():
    """
    Initialize for drawing.  (-700, -700) is in the lower left and
    (600, 600) is in the upper right.
    :pre: pos (0,0), heading (east), up
    :post: pos (0,0), heading (east), up
    :return: None
    """
    turtle.setworldcoordinates(-WINDOW_WIDTH / 2, -WINDOW_WIDTH / 2,
                               WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    turtle.up()
    turtle.title('polygons')
    turtle.speed(0)


def polygon(numSides, sideLength):
    for i in range(0, numSides):
        turtle.forward(sideLength)
        turtle.left(360 / numSides)


def drawart(numShapes, sides, SIDE_LENGTH, isFill, sum):
    sum += numShapes * sides * SIDE_LENGTH
    turtle.pendown()
    colors = ["white", "green", "blue", "black", "yellow", "pink"]
    turtle.pencolor("red")
    for i in range(0, numShapes):
        if isFill:
            turtle.begin_fill()
            turtle.fillcolor(colors[sides - 3])
        polygon(sides, SIDE_LENGTH)
        turtle.left(360 / numShapes)
        if isFill:
            turtle.end_fill()
    if sides == 3:
        print("Sum:")
        print(sum)
        return
    else:
        turtle.penup()
        turtle.left(10)
        turtle.forward(50)
        turtle.pendown()
        drawart(numShapes, sides - 1, SIDE_LENGTH - 10, isFill, sum)


def writename():
    turtle.penup()
    turtle.setpos(-690, 680)
    turtle.pendown()
    turtle.pencolor("black")
    turtle.write("BIKASH ROY", move=False, align="left", font=("Arial", 15, "normal"))
    turtle.setpos(-690, 650)
    turtle.write("TANAY BHARDWAJ", move=False, align="left", font=("Arial", 15, "normal"))
    turtle.penup()


def main():
    init()
    argsv = sys.argv
    if len(argsv) < 3:
        print("Arguments missing, enter Sides followed by Fill or Un-fill")
        return
    number_of_sides = int(argsv[1])
    fill_or_unfill = argsv[2]
    if (number_of_sides > 8) or (number_of_sides < 3):
        print("Number of sides must be within the range of 3 to 8")
        return
    if fill_or_unfill == "fill":
        drawart(30, number_of_sides, SIDE_LENGTH, True, 0)
    else:
        drawart(30, number_of_sides, SIDE_LENGTH, False, 0)
    writename()
    turtle.update()
    turtle.mainloop()


if __name__ == '__main__':
    main()
