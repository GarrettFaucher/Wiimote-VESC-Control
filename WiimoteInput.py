# Code sourced from
# https://www.raspberrypi-spy.co.uk/2013/02/nintendo-wii-remote-python-and-the-raspberry-pi/
# Modified by Garrett Faucher and Shauna Kimura

import cwiid
import time
import sys

# sendData method takes a string as input.
# Performs like normal print statement, but also flushes for main.js too
def sendData(words):
    print words.decode('utf-8')
    sys.stdout.flush()

button_delay = 0.1

sendData('CONNECT_NOW')
time.sleep(1)

# Connect to the Wii Remote. If it times out then quit.
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  quit()

# Rumble for tactile signal that controller has been connected.
wii.rumble = 1
time.sleep(0.4)
wii.rumble = 0
sendData('CONNECTED')

wii.rpt_mode = cwiid.RPT_BTN

while True:

  buttons = wii.state['buttons']

  # If Plus and Minus buttons pressed together then rumble and quit.
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    sendData('DISCONNECTED')
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)

  # Check if other buttons are pressed by doing a bitwise AND of the buttons
  # number and the predefined constant for that button.
  if (buttons - cwiid.BTN_LEFT - cwiid.BTN_B == 0):
    sendData('LEFT')
    time.sleep(button_delay)

  if (buttons - cwiid.BTN_RIGHT - cwiid.BTN_B == 0):
    sendData('RIGHT')
    time.sleep(button_delay)

  if (buttons - cwiid.BTN_UP - cwiid.BTN_B == 0):
    sendData('UP')
    time.sleep(button_delay)

  if (buttons - cwiid.BTN_DOWN - cwiid.BTN_B == 0):
    sendData('DOWN')
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

  if (buttons & cwiid.BTN_HOME):
    sendData('HOME')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_MINUS):
    sendData('MINUS')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_PLUS):
    sendData('PLUS')
    time.sleep(button_delay)
