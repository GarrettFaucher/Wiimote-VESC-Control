import subprocess
import sys

# run the command `python wiiMonitor.py` as a child process
# stdoud and stderr parameters tell the child process where to send output and errors
# in this case we want everything sent to pipe, so that we can read it later on within the program
wiiMonitor = subprocess.Popen(
    'python3 WiimoteInput.py', stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

while True:
    #read stdout (output) from your process
    out = wiiMonitor.stdout.read(1)
    #if there is no new output, do nothing
    if out == '' and wiiMonitor.poll() != None:
        break
    #if there is new output from the child process
    if out != '':
        #save the output from the child process
        newOutput = out.decode('utf-8');
        #print the output that we got from the child process
        sys.stdout.write('wiiMonitor output:'+newOutput)
        #flush the main processes output so that the console will show the new output
        sys.stdout.flush()
