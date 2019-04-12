# Code sourced from
# https://www.raspberrypi-spy.co.uk/2013/02/nintendo-wii-remote-python-and-the-raspberry-pi/
# Modified by Garrett Faucher and Shauna Kimura

import cwiid
import time

button_delay = 0.1

print 'Press 1 + 2 on your Wiimote now...'
time.sleep(1)

# Connect to the Wii Remote. If it times out
# then quit.
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Error opening wiimote connection"
  quit()

print 'Wii Remote connected...\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

wii.rpt_mode = cwiid.RPT_BTN

while True:

  buttons = wii.state['buttons']

  # If Plus and Minus buttons pressed
  # together then rumble and quit.
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    print '\nClosing connection ...'
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)

  # Check if other buttons are pressed by
  # doing a bitwise AND of the buttons number
  # and the predefined constant for that button.
  if (buttons & cwiid.BTN_LEFT):
    print 'Left'
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_RIGHT):
    print 'Right'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_UP):
    print 'Up'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_DOWN):
    print 'Down'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_1):
    print '1'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_2):
    print '2'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_A):
    print 'A'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_B):
    print 'B'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_HOME):
    print 'Home'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_MINUS):
    print 'Minus'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_PLUS):
    print 'Plus'
    time.sleep(button_delay)
