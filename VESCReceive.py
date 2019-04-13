# Code for Rasberry Pi to interface with a VESC using a Wiimote

import time
import sys
import threading
import subprocess
import cwiid
import pigpio
import pyvesc

# Global Variables
WIIMOTE_MAC = "00:1C:BE:25:8B:36"
POWER_DOWN = ["sudo", "shutdown", "-h", "now"]

# ???
BRAKE = pyvesc.SetCurrentBrake(1)
SPEED_ONE = pyvesc.SetDutyCycle(100)
SPEED_TWO = pyvesc.SetDutyCycle(1000)
SPEED_THREE = pyvesc.SetDutyCycle(10000)
SPEED_FOUR = pyvesc.SetDutyCycle(100000)
