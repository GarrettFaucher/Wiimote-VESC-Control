# Starts WiiMoteInput.py, pipe.js, and VESCReciever in a monitored environment through pm2
# If the software crashes, pm2 will restart the script immediately
# Run this file from /etc/rc.local on Raspberry Pi bootup

pm2 start VESCReceive.py -n "Wiimote-VESC-Control"
