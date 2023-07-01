# This is a simple example on how to use the AX1 robotic arm.
# The example is specific for the game pegs but can be applied
# to any other creative applications.

from AX1 import Arm  # Import the arm library

RobotArm = Arm("COM5") # Create an instance of a robot arm to control and define the COM port it is located


# Define what you would like the arm to do

RobotArm.PickUp(2) # PickUp(#) - Pick up a playing piece on the board from a position
RobotArm.PutDown(3) # PutDown(#) - Once a piece has been picked up, put the piece down somewhere


# For the AX-1 pegs game, the position 1 will throw the part off the board.
RobotArm.PickUp(3) # Pick up from square 2
RobotArm.PutDown(1) # Take piece off the game board
RobotArm.home() # Send arm back to home position (Set in AX1.py)


# Set servo positions for each axis individually
# (Rotation, Top joint, Base Joint, Gripper)
# Let's open and close the gripper 3 times from home position
RobotArm.move_it((80,100,100,90))
RobotArm.home()
RobotArm.move_it((80,100,100,90))
RobotArm.home()
RobotArm.move_it((80,100,100,90))
RobotArm.home()