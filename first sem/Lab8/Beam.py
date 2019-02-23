'''
Balance.py
This program creates a balance puzzle from
an input file, solves any missing weights, and
draws the balance puzzle using the turtle.
'''

__author__ = 'Bikash Roy'

import turtle

# Length of line between beams
BEAM_LEVEL = 30

# Length of line to a weight
WEIGHT_LEVEL = 20

# Minimum amount of pixels needed between
# two things hanging from a beam
MINIMUM_SPACE = 20

# Right hand turn
RIGHT_AN = 90

# Degrees for Southward heading
SOUTH = 270

# Screen length
SCREEN_LENGTH = 400

# Screen width
SCREEN_WIDTH = 400

# This class simulates a weight hanging from
# a beam. It has a weight, and a distance from
# the balance's center. It has a zero length
# left and right extent and no pixel scale.
class Weight:

    # The slots for this class. They cover the different
    # aspects of the weight.
    __slots__ = 'weight', 'distance', 'left', 'right', 'scale'

    def __init__(self, distance, weight ):
        """
        The __init__ method. It initializes the distance of this
        weight from the center of the beam and the weight's weight
        value. It also sets its left, right, and scale values to zero.
        :param distance: the distance of this weight from the center
                         of the beam
        :param weight:   the weight of this weight
        :return: None
        """
        self.weight = weight
        self.distance = distance
        self.left = 0
        self.right = 0
        self.scale = 0

    def scaleFactor(self):
        """
        Although this weight object has zero length
        left and right extents, this method is included
        for the recursive method of the same name in the
        beam class.
        :return: the left and right extents ( each are zero )
        """
        return self.left, self.right

    def solveWeights(self):
        """
        This method returns the weight of this weight object.
        :return: the weight of this weight object
        """
        return self.weight

    def draw(self):
        """
        This method uses the turtle to draw the weight
        as a single vertical line with its weight value
        written below.
        :return: None
        :pre: Pos( Some position along the beam that it hangs
                    from, relative to the origin) Heading( South )
        :post: Pos( Some position along the beam that it hangs
                    from, relative to the origin) Heading( South )
        """

        # Draw the vertical line
        turtle.forward(WEIGHT_LEVEL)
        turtle.up()

        # Move forward just enough so that the
        # text is just below the line
        turtle.forward(10)
        turtle.down()

        # Use the turtle write command to write
        # the weight below the line. "align" is set
        # to 'center' so that the text will be right
        # below the line.
        turtle.write(str(self.weight), align = 'center')

        # Move back to the beginning
        turtle.up()
        turtle.back(10)
        turtle.down()
        turtle.back(WEIGHT_LEVEL)

# This class simulates a beam in a balance puzzle. It extends
# some number of units of distance, referred to as ticks, to the
# left and right, has weights and/or othe beams hanging from it.
# If it has a weight with a negative value, it solves for what weight
# would balance the puzzle.
class Beam:

    # The values needed for each beam.
    __slots__ = 'name', 'left', 'right', 'distance', 'hanging', 'scale', 'weight'

    def __init__(self, name ):
        """
        The __init__ method, it initializes the name of the beam,
        which is used in constructing the larger puzzle, and the
        other values needed by the beam.
        :param name: the name of this beam
        :return: None
        """

        # The name of the beam
        self.name = name

        # The objects hanging from this beam
        self.hanging = list()

        # Left and right extents of the beam
        self.left = 0
        self.right = 0

        # Distance from the beam above this one
        self.distance = 0

        # The number of pixels per tick
        self.scale = 1

        # The weight of this beam, composed of the sum
        # of the weights hanging from it
        self.weight = 0

    def add(self, hanger ):
        """
        This method adds an object to the list of objects
        hanging from this beam
        :param hanger: an object hanging from this beam
        :return: None
        """
        self.hanging.append( hanger )

    def scaleFactor(self):
        """
        This method determines an appropriate scale factor
        value for this beam; that is, how many pixels per tick
        mark so that everything hanging from it, all the way
        down to the bottom, are at least 20 pixels apart. It does
        so recursively by calling this method on every object hanging
        from it. The base case is when this method is called on
        a Weight object.
        :return: sum of the left extends and sum of the right extents
        """

        # The sum of the left and right
        # extents of all beams below this one
        farLeft = 0
        farRight = 0

        # The greatest tick mark length
        # calculated for this beam so far
        greatest = 0

        # Loop over the beams and weights hanging from
        # This particular beam.
        for index in range( len(self.hanging) - 1 ):

            # Make recursive calls on the two objects under
            # consideration.
            leftLeft, leftRight = self.hanging[index].scaleFactor()
            rightLeft, rightRight = self.hanging[index+1].scaleFactor()

            # Keep track of the sum of the left extents
            if index == 0:
                farLeft = leftLeft

            # Keep track of the sum of the right extents
            elif index == len(self.hanging) - 2:
                farRight = rightRight

            # Calculate the total distance needed for this two
            # objects to be at least 20 pixels apart from each other
            total = abs(leftRight) + MINIMUM_SPACE + abs(rightLeft)

            # Divide the calculated value by the number of tick
            # marks between the two objects
            totalPerTick = total / ( abs( ( self.hanging[index].distance * -1 ) +
                                          self.hanging[index + 1].distance ) )

            # If the calculated number of pixels per tick mark
            # is greater than the one on record for this object,
            # then update the one on record to this one.
            if totalPerTick > greatest:
                greatest = totalPerTick

        # Set the scale factor ( pixels per tick ) to the
        # value calculated above
        self.scale = greatest

        # Multiply the left and right number of tick
        # marks by the scale factor
        self.left = self.left * self.scale
        self.right = self.right * self.scale

        # Return the left sum of all left extents so far,
        # and the sum of all right extents so far
        return self.left + farLeft, self.right + farRight

    def solveWeights(self):
        """
        This method checks all weights in the balance puzzle.
        If it encounters a weight of negative one, it calculates
        the correct weight to balance the puzzle and changes the
        negative weight to that value. It does so recursively. The
        base case is when this method is called on a Weight object.
        :return: the weight of this object
        """

        # Total weight of the beam
        totalWeight = 0

        # Sum of the left torques
        leftTorqueSum = 0

        # Sum of the right torques
        rightTorgueSum = 0

        # A pointer to the hanging object with -1 weight
        empty = None

        # What the correct weight for the -1 weight
        # should be
        correct = 0

        # Loop over everything hanging from this beam
        for hang in self.hanging:

            # Find the weight of the object
            weight = hang.solveWeights()

            # If the weight is negative, then we
            # need to solve it to balance the beam
            if weight < 0:
                empty = hang
            else:

                # Add the weight to the total of this beam
                totalWeight = totalWeight + weight

                # If the weight is to the left
                if hang.distance < 0:
                    leftTorqueSum = leftTorqueSum + ( weight * hang.distance )

                # If not to the left, it must be to the right
                else:
                    rightTorgueSum = rightTorgueSum + ( weight * hang.distance )

        # If there was a weight with -1 weight, add left and right
        # torque sums together and divide by the distance from the
        # center to the weight with -1 weight. This will be the correct
        # weight to balance the beam
        if empty != None:
            correct = abs( ( leftTorqueSum + rightTorgueSum ) / empty.distance )
            empty.weight = correct

        # The weight of a beam is the sum of the weights hanging
        # from it.
        self.weight = totalWeight + correct

        return self.weight

    def draw(self):
        """
        This method draws the beam that it is called
        on and all weights hanging from it. It does so recursively.
        The base case is when this method is called on a
        Weight object. To draw the entire puzzle, we would call
        this method on the head of the puzzle, the top most beam.
        :return: None
        :pre (for first call): Pos ( 0, 0 ) Heading( East )
        :pre: Pos( Some position along the beam that it hangs
                    from, relative to the origin) Heading( South )
        :post: Pos( Some position along the beam that it hangs
                    from, relative to the origin) Heading( South )
        """

        # The turtle must always start by facing south
        turtle.setheading(SOUTH)

        # Draw a vertical line downward from the beam
        # above
        turtle.forward( BEAM_LEVEL )

        # Position in this beams list of hanging objects
        index = 0

        # Turn to draw the left hanging objects
        turtle.right( RIGHT_AN )

        # So long as there are objects to draw, and they
        # are on the left hand side of the beam, keep going
        while index != len( self.hanging ) and int(self.hanging[index].distance) < 0:

            # Draw out to where the object hangs from the beam
            turtle.forward( ( self.hanging[index].distance * -1 ) * self.scale )
            turtle.left( RIGHT_AN )

            # Make a recursive call upon the object
            # hanging from this beam
            self.hanging[index].draw()
            turtle.right( RIGHT_AN )

            # Move back
            turtle.back( ( self.hanging[index].distance * -1 ) * self.scale )

            # Increment the value of the index
            index = index + 1

        # Turn to draw the right hanging objects
        turtle.right( 180 )

        # So long as there are objects to draw, and they
        # are on the right hand side of the beam, keep going
        while index != len( self.hanging ) and int(self.hanging[index].distance) > 0:

            # Draw out to where the object hangs from the beam
            turtle.forward( self.hanging[index].distance * self.scale )
            turtle.right( RIGHT_AN )

            # Make a recursive call upon the object
            # hanging from this beam
            self.hanging[index].draw()
            turtle.left( RIGHT_AN )

            # Move back
            turtle.back( self.hanging[index].distance * self.scale )

            # Increment the value of the index
            index = index + 1

        # Move the turtle back to where it started
        turtle.right( RIGHT_AN )
        turtle.back( BEAM_LEVEL )


def setUp(fileName):
    """
    This function opens a balance puzzle file,
    creates beam and weight objects according to the
    lines in the file, and creates a balance puzzle
    using those objects.
    :param fileName: the name of the balance puzzle file
    :return: the 'root' beam of the balance puzzle
    """

    # The root beam. Its name is 'B'
    head = None

    # The collection of beams created so far
    beams = list()

    # Open the file
    with open (fileName) as file:

        # Iterate through the lines
        for line in file:

            # Split the line into its components
            weightsAndBeams = line.split()

            # Create a beam object
            b = Beam(weightsAndBeams[0])
            beams.append(b)

            # If the name is that of the root beam
            if weightsAndBeams[0] == 'B':
                head = b

            # Iterate over the components
            for component in range( 1, len(weightsAndBeams) , 2 ):

                # Set the beam's leftmost and rightmost distances
                if component == 1:
                    b.left = int(weightsAndBeams[component])
                elif component == len(weightsAndBeams) - 2:
                    b.right = int(weightsAndBeams[component])

                # A flag that records if we found another
                # beam hanging from this one
                found = False

                # Find out if the component is a beam
                for beam in beams:

                    # If it is, set up a link between the new
                    # beam object and this one and set the flag to true
                    if weightsAndBeams[component+1] == beam.name:
                        beam.distance = int(weightsAndBeams[component])
                        b.add( beam )
                        found = True

                # If it is not a beam, it must be a weight
                if not found:
                    w = Weight( int( weightsAndBeams[component] ),
                                int( weightsAndBeams[component+1] ) )
                    b.add( w )
    return head

def turtleSetUp():
    """
    This function sets up the turtle window for drawing.
    :return: None
    :pre: No pre conditions
    :post: Pos( 0, 0 ) Heading( east )
    """
    turtle.screensize( SCREEN_WIDTH, SCREEN_LENGTH )
    turtle.setworldcoordinates( -SCREEN_WIDTH/2, -SCREEN_LENGTH/2,
                                SCREEN_WIDTH/2, SCREEN_LENGTH/2 )
    turtle.speed(0)

def main():
    """
    The main function. It uses a file name
    to create a balance puzzle, solves for any
    -1 weights in the puzzze, and then draws it
    using the turtle.
    :return: None
    """

    # The name of the balance puzzle file
    fileName = 'balance'

    # Opens the file and builds the balance puzzle.
    # The 'root' beam of the puzzle is returned
    b = setUp(fileName)

    # Finds the scale factor for each beam
    b.scaleFactor()

    # Finds any missing weights
    b.solveWeights()

    # Sets up the turtle window and begins drawing
    turtleSetUp()
    b.draw()
    turtle.mainloop()

if __name__ == '__main__':
    main()