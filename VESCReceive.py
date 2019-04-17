# Code for Rasberry Pi to interface with a VESC using a Wiimote

import time
#import sys
#import threading
#import subprocess
import pigpio
import pyvesc
import sys
from subprocess import Popen, PIPE
from threading  import Thread
from queue      import Queue, Empty

# Global Variables
WIIMOTE_MAC = "00:1C:BE:25:8B:36"
POWER_DOWN = ["sudo", "shutdown", "-h", "now"]

# EXPERIMENTAL CODE ALL BELOW
BRAKE = pyvesc.SetCurrentBrake(1)
SPEED_ONE = pyvesc.SetDutyCycle(100)
SPEED_TWO = pyvesc.SetDutyCycle(1000)
SPEED_THREE = pyvesc.SetDutyCycle(10000)
SPEED_FOUR = pyvesc.SetDutyCycle(100000)

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


// Motor Control
while True:
    // Brake
    if OUTPUT.A == pressed:
        pyvesc.SetCurrentBrake(???)
    if OUTPUT.B == pressed and OUTPUT.DOWN == pressed:
        pyvesc.
    
