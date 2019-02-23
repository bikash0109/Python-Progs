__author__ = 'BR'
__author__ = 'TB'

"""
Author: BIKASH ROY
Author: TANAY BHARDWAJ

File name: polygons.py
"""
import turtle
import sys


def init():
    """
    Initialize for drawing.  (-700, -700) is in the lower left and
    (700, 700) is in the upper right.
    :pre: pos (0,0), heading (east), up
    :post: pos (0,0), heading (east), up
    :return: None
    """
    turtle.setworldcoordinates(-1400 / 2, -1400 / 2,
                               1400 / 2, 1400 / 2)
    turtle.up()
    turtle.title('polygons')
    turtle.tracer(0, 0)
    write_name()


def write_name():
    """
    prints the team members' name on the top left hand side corner of the window.
    :pre: pos (0,0), heading (east), up
    :post: pos (0,0), heading (east), up
    :return: None
    """
    turtle.setpos(-690, 670)
    turtle.pendown()
    turtle.pencolor("red")
    turtle.write("Bikash Roy", align="left", font=("Arial", 15))
    turtle.setpos(-690, 630)
    turtle.write("Tanay Bhardwaj", align="left", font=("Arial", 15))
    turtle.penup()
    turtle.pencolor("black")
    turtle.home()


def draw_polygon(sides, side_length, is_fill, sum):
    """
    draws polygons recursively.
    :pre: pos (0,0), heading (east), up
    :post: pos (0,0), heading (east), up
    for cosmetics, it draws a circle at each end of the polygon.
    :return: None
    """
    sum += sides * sides * side_length
    turtle.pendown()
    for i in range(0, sides):
        if is_fill:
            turtle.begin_fill()
            turtle.fillcolor("gray" if sides % 2 == 0 else "white")
        for j in range(0, sides):
            turtle.pencolor("black")
            turtle.forward(side_length)
            turtle.forward(50)
            turtle.circle(10)
            turtle.backward(50)
            turtle.left(360 / sides)
        turtle.left(360 / sides)
        if is_fill:
            turtle.end_fill()
    if sides == 3:  # exit condition
        turtle.penup()
        print('Sum: ', sum)
        return  # comes out of the loop
    else:
        draw_polygon(sides - 1, side_length - 20, is_fill, sum)


def main():
    """
    The main function.
    :pre: pos (0,0), heading (east), up
    :post: pos (0,0), heading (east), up
    :return: None
    """
    init()
    arguments = sys.argv
    if len(arguments) < 3:
        print("Arguments missing, enter Sides followed by Fill or Un-fill")
        return
    number_of_sides = int(arguments[1])
    fill_or_un_fill = arguments[2]
    if (number_of_sides > 8) or (number_of_sides < 3):
        print("Number of sides must be within the range of 3 to 8")
        return
    if fill_or_un_fill == "fill":
        draw_polygon(number_of_sides, 200, True, 0)  # side_length = 200
    else:
        draw_polygon(number_of_sides, 200, False, 0)  # side_length = 200
    turtle.update()
    turtle.mainloop()


if __name__ == '__main__':
    main()
