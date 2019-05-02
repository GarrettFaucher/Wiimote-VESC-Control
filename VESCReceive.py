#!/usr/bin/env python3

# Code for Rasberry Pi to interface with a VESC using a Wiimote

import time
import serial
import pyvesc
import sys
from subprocess import Popen, PIPE
from threading  import Thread
from queue      import Queue, Empty

# Global Variables
POWER_DOWN = ["sudo", "shutdown", "-h", "now"]

# Constants for Accel and Brake
BRAKE_ONE = 10000
BRAKE_TWO = 20000
BRAKE_THREE = 30000
BRAKE_FOUR = 50000
SPEED_ONE = 10000
SPEED_TWO = 20000
SPEED_THREE = 30000
SPEED_FOUR = 50000
STOP = 0

DIV_CONST = 15
SLEEP_TIME = 0.0001

# Create a serial object to send serial messages
ser = serial.Serial(
    port='/dev/serial0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Function to read input
def enqueueOutput(out, queue):
    while True:
        lines = out.readline().decode('utf-8')
        out.flush()
        queue.put(lines)

# Function to simplify the serial output for changing duty cycles
def changeDuty(num):
    ser.write(pyvesc.encode(pyvesc.SetDutyCycle(num)))
    time.sleep(SLEEP_TIME)

# Function to simplify the serial output for changing brake
def changeBrake(num):
    ser.write(pyvesc.encode(pyvesc.SetCurrentBrake(num)))

# Function to simplify the gradual increase of speed if stepping up
def stepUp(speedStart, speedEnd):
    for i in range(int(speedStart/DIV_CONST), int(speedEnd/DIV_CONST)):
        changeDuty(i*DIV_CONST)
        try:
            newInput = str(queue.get_nowait()).rstrip()
        except Empty:
            continue
        else:
            sys.stdout.write(newInput + "\n")
            sys.stdout.flush()

        if newInput == "A":
            break



# Starting the input process and thread
process = Popen(['/usr/bin/node', 'pipe.js'], stdout=PIPE)
queue = Queue()
enqueueOutputThread = Thread(target=enqueueOutput, args=(process.stdout, queue))
enqueueOutputThread.daemon = True
enqueueOutputThread.start()

oldInput = ""
go = True
tick = 0

# Motor Control
while True:
    # Get new input
    try:
        newInput = str(queue.get_nowait()).rstrip()
    except Empty:
        continue
    else:
        sys.stdout.write(newInput + "\n")
        sys.stdout.flush()

    # Is it Brake or Accel?
    if newInput == "A" and go and tick == 0:
        go = False
        tick = 4
    elif newInput == "A" and not go and tick == 0:
        go = True
        tick = 4

    #Brake Mode
    if not go:
        changeBrake(10)
        if newInput == "DOWN":
            changeBrake(BRAKE_ONE)
        if newInput == "LEFT":
            changeBrake(BRAKE_TWO)
        if newInput == "UP":
            changeBrake(BRAKE_THREE)
        if newInput == "RIGHT":
            changeBrake(BRAKE_FOUR)

    #Accel Mode
    if go:
        # Speed 1
        if newInput == "DOWN":
            changeDuty(SPEED_ONE)

        # Speed 2
        if newInput == "LEFT":
            if oldInput == "DOWN":
                stepUp(SPEED_ONE, SPEED_TWO)
            else:
                changeDuty(SPEED_TWO)

        # Speed 3
        if newInput == "UP":
            if oldInput == "LEFT":
                stepUp(SPEED_TWO, SPEED_THREE)
            elif oldInput == "DOWN":
                stepUp(SPEED_ONE, SPEED_THREE)
            else:
                changeDuty(SPEED_THREE)

        # Speed 4
        if newInput == "RIGHT":
            if oldInput == "UP":
                stepUp(SPEED_THREE, SPEED_FOUR)
            elif oldInput == "LEFT":
                stepUp(SPEED_TWO, SPEED_FOUR)
            elif oldInput == "DOWN":
                stepUp(SPEED_ONE, SPEED_FOUR)
            else:
                changeDuty(SPEED_FOUR)

    # Emergency off switch
    if newInput == "HOME":
            changeDuty(STOP)

    # If controller is disconnected stop the script
    if newInput == "DISCONNECTED":
        exit()

    oldInput = newInput

    if tick > 0:
        tick -= 1
