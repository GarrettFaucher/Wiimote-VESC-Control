var fs = require('fs'); //require filesystem module
const {PythonShell} = require('python-shell');

var wiiFilePath = 'WiimoteInput.py';

function handleWiiData(message){
  console.log("Handling data: "+message);
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
