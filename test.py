import turtle

def koch(t, order, size):
    """
       Make turtle t draw a Koch fractal of 'order' and 'size'.
       Leave the turtle facing the same direction.
    """

    if order == 0:                  # The base case is just a straight line
        t.forward(size)
    else:
        koch(t, order-1, size/3)   # go 1/3 of the way
        t.left(60)
        koch(t, order-1, size/3)
        t.right(120)
        koch(t, order-1, size/3)
        t.left(60)
        koch(t, order-1, size/3)

fred = turtle.Turtle()
wn = turtle.Screen()

fred.color("blue")
wn.bgcolor("green")
fred.penup()
fred.backward(150)
fred.pendown()

koch(fred, 3, 300)

wn.exitonclick()