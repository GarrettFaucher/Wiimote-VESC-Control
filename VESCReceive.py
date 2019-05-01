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

# Time for iteration to next speed
SLEEP_TIME = 0.0001

# Create a serial object to send serial messages
ser = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def enqueueOutput(out, queue):
    while True:
        lines = out.readline().decode('utf-8')
        out.flush()
        queue.put(lines)

def changeDuty(num):
    ser.write(pyvesc.encode(pyvesc.SetDutyCycle(num)))

def changeBrake(num):
    ser.write(pyvesc.encode(pyvesc.SetCurrentBrake(num)))

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
    try:
        newInput = str(queue.get_nowait()).rstrip()
    except Empty:
        continue
    else:
        sys.stdout.write(newInput)
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
        if newInput == "DOWN":
            changeDuty(SPEED_ONE)

        if newInput == "LEFT":
            if oldInput == "DOWN":
                for i in range(SPEED_ONE/10, SPEED_TWO/10):
                    changeDuty(i)
            changeDuty(SPEED_TWO)

        if newInput == "UP":
            if oldinput == "LEFT":
                for i in range(SPEED_TWO/10, SPEED_THREE/10):
                    changeDuty(i)
            if oldInput == "DOWN":
                for i in range(SPEED_ONE/10, SPEED_THREE/10):
                    changeDuty(i)
            changeDuty(SPEED_THREE)

        if newInput == "RIGHT":
            if oldinput == "UP":
                for i in range(SPEED_THREE/10, SPEED_FOUR/10):
                    changeDuty(i)
            if oldinput == "LEFT":
                for i in range(SPEED_TWO/10, SPEED_FOUR/10):
                    changeDuty(i)
            if oldinput == "DOWN":
                for i in range(SPEED_ONE/10, SPEED_FOUR/10):
                    changeDuty(i)
            changeDuty(SPEED_FOUR)

    if newInput == "HOME":
            changeDuty(STOP)

    if tick > 0:
        tick -= 1

    oldInput = newInput
