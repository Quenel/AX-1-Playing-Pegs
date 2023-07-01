import serial
from serial import Serial
import time


class Arm:
    def __init__(self, COM, baud = 9600, timeout = 1):
        # Define serial settings for communication
        self.COM = COM
        self.baud = baud
        self.timeout = timeout
        self.rotation_adjust = 0 # Use this if the rotational servo drifts position
        self.current = (80,100,100,50) #Initial starting position of the arm

        # Connect to the arm
        try:
            self.ser = serial.Serial(COM, 9600, timeout=1)
            print("Arm is successfully connected.")
            self.initiate()
            
            time.sleep(2)
        except Exception as e:
            print("There was an error while trying to connect.")
            print(str(e))

    def home(self):
        self.move_it((80,100,100,50))

    def initiate(self):
        # Initiates the starting position of the arm (set in constructor of class)
        self.current = self.move_it(self.current, self.current)
        print(f"Moved to initial position : {self.current}")
        

    def config(self):
        print(f"COM port: {self.COM}")
        print(f"BAUD rate: {self.baud}")

    def move_it(self, target, sleep_time=0.01):
        while round(self.current[0]) != target[0] or round(self.current[1]) != target[1] or round(self.current[2]) != target[2] or round(self.current[3]) != target[3]:
            self.current = self.next_position(target, 0.1, 1)
            pos = (round(self.current[0]),round(self.current[1]),round(self.current[2]),round(self.current[3]))
            print(pos)
            time.sleep(sleep_time)
            posString = str(pos[0]) + ',' + str(pos[1]) + ',' + str(pos[2]) + ',' + str(pos[3]) + '\n'
            self.ser.write(posString.encode())
            print(pos)
        return self.current
    

    # This function will return the input in the correct direction with one increment based on step size
    def calculate_new(self, end_pos, current_pos, step_size):
        if end_pos > current_pos:
            value = current_pos + step_size
            return value
        if end_pos < current_pos:
            value = current_pos - step_size
            return value
        if end_pos == current_pos:
            return current_pos

    def serial_instance(self):
        return self.ser

    # This function will return a tuple of the next step size (a,b,c,d)
    # check each variable and sent the current and target to calculate_new function
    def next_position(self,targets, speed=0.2, stepSize=0.5):
        newa = None
        newb = None
        newc = None
        newd = None
        if targets[0] != self.current[0] or targets[1] != self.current[1] or targets[2] != self.current[2] or targets[3] != self.current[3]:
            newa =self.calculate_new(targets[0], self.current[0], stepSize)
            newb =self.calculate_new(targets[1], self.current[1], stepSize)
            newc =self.calculate_new(targets[2], self.current[2], stepSize)
            newd =self.calculate_new(targets[3], self.current[3], stepSize)

        new_position = (newa, newb, newc, newd)
        return new_position
    

    # Pick up an item on the playing board
    def PickUp(self, pos):
        # Determine where the arm needs to rotate to
        rotate = 0
        if pos == 1:
            rotate = 160 -self.rotation_adjust
        if pos == 2:
            rotate = 140-self.rotation_adjust
        if pos == 3:
            rotate = 120-self.rotation_adjust
        if pos == 4:
            rotate = 101
        if pos == 5:
            rotate = 77-self.rotation_adjust
        if pos == 6:
            rotate = 58-self.rotation_adjust
        if pos == 7:
            rotate = 37-self.rotation_adjust
        if pos == 8:
            rotate =18-self.rotation_adjust
        
        # Motion required to pick up a piece off the board
        target=(rotate,120,100,60)
        self.current = self.move_it(target)
        target=(rotate,140,100,60)
        self.current = self.move_it(target, 0.02)
        target=(rotate,140,85,60)
        self.current = self.move_it(target, 0.02)
        target=(rotate,140,85,85)
        self.current = self.move_it(target,  0.1)
        target=(rotate,100,100,85)
        self.current = self.move_it(target)
       

    # Put down an item on the playing baord
    def PutDown(self, pos):
        # Get rotational position required
        rotate = 0
        if pos == 1:
            rotate = 160
        if pos == 2:
            rotate = 140
        if pos == 3:
            rotate = 120
        if pos == 4:
            rotate = 100
        if pos == 5:
            rotate = 80
        if pos == 6:
            rotate = 60
        if pos == 7:
            rotate = 40
        if pos == 8:
            rotate = 20

        # Perform the put down sequence
        target=(rotate,100,100,80)
        self.current = self.move_it(target, 0.05)
        target=(rotate,140,85,85)
        self.current = self.move_it(target, 0.05)
        target=(rotate,140,85,60)
        self.current = self.move_it(target, 0.1)
        target=(rotate,100,100,60)
        self.current = self.move_it(target, 0.05)
 

        

    # Function to make a move depending on the instruction
    def robot_make_move(self, command):
        print(command)
   
        self.PickUp(command[0]+2)
        if command[1] == "R":
            self.PutDown(command[0]+4)
            self.PickUp(command[0]+3)
            self.PutDown(1)
            
        if command[1] == "L":
            self.PutDown(command[0])
            self.PickUp(command[0]+1)
            self.PutDown(1)
            
    
    # Go back to initial position
    def end(self):
        rotate = 180
        
        target=(rotate,100,100,80)
        self.move_it(target,  0.05)
        target=(80,100,100,80)
        self.move_it(target)
        target=(80,100,100,50)
        self.move_it(target)