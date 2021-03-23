# 6.00.2x Problem Set 2: Simulating robots

import math
import random
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np 
import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
from ps2_verify_movement37 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
#from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        if height>0 and height>0:
            self.width=width
            self.height=height
        else:
            raise ValueError("Uno de los valores es 0")
            
        self.matriz_rec=np.ones((self.width,self.height))
        
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        if pos.getX()<self.width or pos.getY()<self.height:
            self.matriz_rec[int(pos.getX()),int(pos.getY())]=0                          
        else:
            raise ValueError("La posición No existe en la matriz")


    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.matriz_rec[m,n]==0:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return int(self.width*self.height-np.sum(self.matriz_rec))
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        m=random.randrange(self.width)
        n=random.randrange(self.height)
        return Position(m,n)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if round(pos.getX()) <(self.width) and round(pos.getY())<(self.height):
            if pos.getX()>=0 and pos.getY()>=0:
                return True
            else:
                return False
        else:
            return False

    # === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room=room
        self.speed=speed
        self.direccion=random.randrange(360)
        n=random.randrange(room.width)
        m=random.randrange(room.height)
        self.posicion=Position(n,m)
        self.room.cleanTileAtPosition(self.posicion)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.posicion
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direccion
            
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.posicion=Position(position.getX(),position.getY())


    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direccion=direction
        
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError
        
# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        obt_pos=self.posicion.getNewPosition( self.direccion, self.speed)
        self.room.isPositionInRoom(obt_pos)

        if self.room.isPositionInRoom(obt_pos):
            self.posicion=obt_pos
            Limpiar=self.room.cleanTileAtPosition(self.posicion)
           
        else:
            self.direccion=random.randrange(360)

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        obt_pos=self.posicion.getNewPosition( self.direccion, self.speed)
        self.room.isPositionInRoom(obt_pos)

        if self.room.isPositionInRoom(obt_pos):
            self.posicion=obt_pos
            Limpiar=self.room.cleanTileAtPosition(self.posicion)
            self.direccion=random.randrange(360)
        else:
            self.direccion=random.randrange(360)



#testRobotMovement(StandardRobot, RectangularRoom)
testRobotMovement(RandomWalkRobot, RectangularRoom)
#c=StandardRobot(RectangularRoom(4,4),1)
#e=RectangularRoom(4,4)
#Position(2,2)
#e.isPositionInRoom(d)



            
