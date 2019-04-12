var fs = require('fs'); //require filesystem module
const {PythonShell} = require('python-shell');

var wiiFilePath = 'WiimoteInput.py';

function handleWiiData(message){
  switch (message) {
   case 'LEFT':

      break;

   case 'RIGHT':

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

function monitorWiimote(){
  let options = {
    pythonPath: 'python2',
    scriptPath: './'
  };

  let pyshell = new PythonShell(wiiFilePath, options);

  pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    handleWiiData(message);
  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err,code,signal) {
    monitorWiimote() //relaunch since stopped
  });
}

monitorWiimote(); //run WiimoteInput.py and send any output to handleWiiData()
