# Code for Rasberry Pi to interface with a VESC using a Wiimote

import time
import serial
import pyvesc
import sys
import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
from threading  import Thread
from queue      import Queue, Empty

# Global Variables
WIIMOTE_MAC = "00:1C:BE:25:8B:36"
POWER_DOWN = ["sudo", "shutdown", "-h", "now"]
GPIO_OUT = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_OUT, GPIO.OUT)

GPIO.output(GPIO_OUT, pyvesc.SetCurrentBrake(1))

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
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def printOutput(message):
    print()

def enqueue_output(out, queue):
    while True:
        lines = out.readline()
        out.flush()
        queue.put(lines)

process = Popen(['/usr/bin/node', 'pipe.js'], stdout=PIPE)
queue = Queue()
thread = Thread(target=enqueue_output, args=(process.stdout, queue))
thread.daemon = True
thread.start()

while True:
    try:
        newInput = queue.get_nowait()
    except Empty:
        continue
    else:
        sys.stdout.write(str(newInput))
        sys.stdout.flush()

go = True
# Motor Control
while True:
    # Is it Brake or Accel?
    if OUTPUT.A == pressed and go:
        go = False
    if OUTPUT.A == pressed and not go:
        go = True

    #Brake Mode
    if not go:
        if OUTPUT.B == pressed and OUTPUT.BTN_DOWN == pressed:
            ser.write(pyvesc.encode(BRAKE_ONE))
        if OUTPUT.B == pressed and OUTPUT.BTN_LEFT == pressed:
            ser.write(pyvesc.encode(BRAKE_TWO))
        if OUTPUT.B == pressed and OUTPUT.BTN_UP == pressed:
            ser.write(pyvesc.encode(BRAKE_THREE))
        if OUTPUT.B == pressed and OUTPUT.BTN_RIGHT == pressed:
            ser.write(pyvesc.encode(BRAKE_FOUR))
    #Accel Mode
    if go:
        if OUTPUT.B == pressed and OUTPUT.BTN_DOWN == pressed:
            ser.write(pyvesc.encode(SPEED_ONE))
        if OUTPUT.B == pressed and OUTPUT.BTN_LEFT == pressed:
            ser.write(pyvesc.encode(SPEED_TWO))
        if OUTPUT.B == pressed and OUTPUT.BTN_UP == pressed:
            ser.write(pyvesc.encode(SPEED_THREE))
        if OUTPUT.B == pressed and OUTPUT.BTN_RIGHT == pressed:
            ser.write(pyvesc.encode(SPEED_FOUR))
