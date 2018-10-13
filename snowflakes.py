# Python code to draw snowflakes fractal.
import turtle
import random

# setup the window with a background color
wn = turtle.Screen()

# assign a name to your turtle
elsa = turtle.Turtle()
elsa.speed(0)

# create a list of colours
sfcolor = ["white", "blue", "purple", "grey", "magenta"]


# create a function to create different size snowflakes
def snowflake(size):
    # move the pen into starting position
    elsa.penup()
    elsa.forward(10 * size)
    elsa.left(45)
    elsa.pendown()
    elsa.color(random.choice(sfcolor))

    # draw branch 8 times to make a snowflake
    for i in range(8):
        print("Drawing branch of size : ", size)
        branch(size)
        elsa.left(45)

    # create one branch of the snowflake


def branch(size):
    for i in range(1):
        print("Outer i = ", i)
        for i in range(1):
            print("Inner i = ", i)
            elsa.forward(10.0 * size / 3)
            elsa.backward(10.0 * size / 3)
            elsa.right(45)
        elsa.left(90)
        elsa.backward(10.0 * size / 3)
        elsa.left(45)
    elsa.right(90)
    elsa.forward(10.0 * size)


# loop to create 20 different sized snowflakes
# with different starting co-ordinates
for i in range(1):
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)
    sf_size = random.randint(1, 4)
    print(x, ",", y)
    print(sf_size)
    elsa.penup()
    elsa.goto(x, y)
    elsa.pendown()
    snowflake(sf_size)

# leave the window open until you click to close
wn.exitonclick()
