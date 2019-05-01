# Code for Rasberry Pi to interface with a VESC using a Wiimote

import time
import serial
import pyvesc
import sys
from subprocess import Popen, PIPE
from threading  import Thread
from queue      import Queue, Empty

# Global Variables
WIIMOTE_MAC = "00:1C:BE:25:8B:36"
POWER_DOWN = ["sudo", "shutdown", "-h", "now"]

# EXPERIMENTAL CODE ALL BELOW
BRAKE_ONE = pyvesc.SetCurrentBrake(10)
BRAKE_TWO = pyvesc.SetCurrentBrake(100)
BRAKE_THREE = pyvesc.SetCurrentBrake(10000)
BRAKE_FOUR = pyvesc.SetCurrentBrake(100000)
SPEED_ONE = pyvesc.SetDutyCycle(100)
SPEED_TWO = pyvesc.SetDutyCycle(1000)
SPEED_THREE = pyvesc.SetDutyCycle(10000)
SPEED_FOUR = pyvesc.SetDutyCycle(100000)

# Create a serial object to send serial messages
ser = serial.Serial(
    port='/dev/serial0',
    baudrate = 115200,
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

process = Popen(['/usr/bin/node', 'pipe.js'], stdout=PIPE)
queue = Queue()
enqueueOutputThread = Thread(target=enqueueOutput, args=(process.stdout, queue))
enqueueOutputThread.daemon = True
enqueueOutputThread.start()

go = True
i = 0
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
    if newInput == "A" and go and i == 0:
        go = False
        i = 4
    elif newInput == "A" and not go and i == 0:
        go = True
        i = 4

    #Brake Mode
    if not go:
        if newInput == "DOWN":
            ser.write(pyvesc.encode(BRAKE_ONE))
            print("Brake 1")
        if newInput == "LEFT":
            ser.write(pyvesc.encode(BRAKE_TWO))
            print("Brake 2")
        if newInput == "UP":
            ser.write(pyvesc.encode(BRAKE_THREE))
            print("Brake 3")
        if newInput == "RIGHT":
            ser.write(pyvesc.encode(BRAKE_FOUR))
            print("Brake 4")

    #Accel Mode
    if go:
        if newInput == "DOWN":
            ser.write(pyvesc.encode(SPEED_ONE))
            print("Accel 1")
        if newInput == "LEFT":
            ser.write(pyvesc.encode(SPEED_TWO))
            print("Accel 2")
        if newInput == "UP":
            ser.write(pyvesc.encode(SPEED_THREE))
            print("Accel 3")
        if newInput == "RIGHT":
            ser.write(pyvesc.encode(SPEED_FOUR))
            print("Accel 4")

    if i > 0:
        i -= 1
