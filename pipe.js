// pipe.js passes data from WiimoteInput.py to VESCRecieve.py
// Since cwiid is a Python 2 library and pyvesc is a Python 3 library,
// this is needed as they must be seperate files.

var fs = require('fs'); //require filesystem module
const {PythonShell} = require('python-shell'); // Import python-shell

var wiiFilePath = 'WiimoteInput.py'; // Input file name

// Depending on the button pressed on Wiimote, different signals are passed
// to VESCRecieve.py for VESC control.
function handleWiiData(message){
  switch (message) {
   case 'LEFT':

      break;

   case 'RIGHT':
      // ADD A CASE HERE
      break;

   case 'UP':

      break;

   case 'DOWN':

      break;

   case '1':

      break;

   case '2':

      break;

   case 'A':

      break;

   case 'B':

      break;

   case 'HOME':

      break;

   case 'MINUS':

      break;

   case 'PLUS':

      break;

  }
}

// Function to monitor if input is passed from WiimoteInput.py
function monitorWiimote(){
  let options = {
    pythonPath: 'python2', // Specifiying that python2 should be used
    scriptPath: './'
  };

  let pyshell = new PythonShell(wiiFilePath, options);

  pyshell.on('message', function (message) {
    // Received a message sent from the Python script (a simple "print" statement)
    handleWiiData(message);
  });

  // End the input stream and allow the process to exit
  pyshell.end(function (err,code,signal) {
    monitorWiimote() //relaunch since stopped
  });
}

monitorWiimote(); // Run WiimoteInput.py and send any output to handleWiiData()
