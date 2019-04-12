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
