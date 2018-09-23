import turtle
import random
import sys



WINDOW_LENGTH = 800
SIDE_LENGTH = 200
FILL_PEN_WIDTH = 2
UNFILL_PEN_WIDTH = 2

color = ["violet", "black", "green","blue","yellow", "red"]
color = random.choice(color)
turtle.color("black", "yellow")

#side = int(input('Enter side'))

#length = int(input('Enter length'))

def Polygon(side, length):
        turtle.begin_fill()
        for i in range(0, side):
            if side >= 3:
                turtle.pendown()
                turtle.pencolor("black")
            else:
             return false

            #turtle.color("black", "pink")

            #turtle.color("blue")
            turtle.forward(length)
            turtle.left(360/side)
        turtle.forward(3)
        turtle.left(5)
        turtle.forward(length)
        turtle.left(360 / side)
        turtle.forward(length)
        turtle.left(360 / side)

        turtle.end_fill()


        #turtle.backward(20)
        #turtle.right(5)
        #turtle.forward(15)
        #turtle.left(5)
        if length < 1:
            return False
        Polygon(side,length-2)


        turtle.penup()
        turtle.goto(-300,300)
        turtle.pendown()
        turtle.write("BIKASH ROY", move=False, align="left", font=("Arial", 8, "normal"))
        turtle.goto(-300, 290)
        turtle.write("TANAY BHARDWAJ", move=False, align="left", font=("Arial", 8, "normal"))
        turtle.penup()


#turtle.color(color)

turtle.speed(100)
Polygon(8,200)
turtle.update()
turtle.mainloop()


def main():
    Polygon(5,200)
    turtle.update()
    turtle.mainloop()