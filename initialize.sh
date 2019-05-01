# Starts WiiMote listener, pipe, and VESC Reciever in a monitored environment via pm2
# If the software crashes, pm2 will restart the script immediately
# Run this file from /etc/rc.local on raspberrypi bootup

sudo pm2 start VESCReceive.py -n "Wiimote-VESC-Control"
