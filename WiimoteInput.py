

# WIIMOTE MAC 00:1C:BE:25:8B:36
# Code sourced from
# https://www.raspberrypi-spy.co.uk/2013/02/nintendo-wii-remote-python-and-the-raspberry-pi/
# Modified by Garrett Faucher and Shauna Kimura

import cwiid
import time
import sys

def sendData(words):
    print words
    sys.stdout.flush()

button_delay = 0.1

sendData('Press 1 + 2 on your Wiimote now...')
sys.stdout.flush()
time.sleep(1)

# Connect to the Wii Remote. If it times out
# then quit.
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  sendData("Error opening wiimote connection")
  quit()

wii.rumble = 1
time.sleep(0.4)
wii.rumble = 0
sendData('Wii Remote connected...\n')
sendData('Press PLUS and MINUS together to disconnect and quit.\n')

wii.rpt_mode = cwiid.RPT_BTN

while True:

  buttons = wii.state['buttons']

  # If Plus and Minus buttons pressed
  # together then rumble and quit.
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    sendData('\nClosing connection ...')
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)

  # Check if other buttons are pressed by
  # doing a bitwise AND of the buttons number
  # and the predefined constant for that button.
  if (buttons & cwiid.BTN_LEFT):
    sendData('Left')
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_RIGHT):
    sendData('Right')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_UP):
    sendData('Up')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_DOWN):
    sendData('Down')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_1):
    sendData('1')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_2):
    sendData('2')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_A):
    sendData('A')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_B):
    sendData('B')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_HOME):
    sendData('Home')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_MINUS):
    sendData('Minus')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_PLUS):
    sendData('Plus')
    time.sleep(button_delay)
