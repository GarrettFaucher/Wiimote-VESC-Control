var fs = require('fs'); //require filesystem module

var newSensorData = false;

var wiiFilePath = 'WiimoteInput.py';

const {PythonShell} = require('python-shell');

function getWiiData(){
  var wiiMote = new PythonShell(wiiFilePath);
  var foundData;

  return new Promise(function(resolve,reject){
    wiiMote.on('message', function(message){
      resolve(message);
    })

    wiiMote.end(function(err){
      if(err){
        reject(err);
      };
    });
  });

}

setInterval(function(){
  var wiiGetter = getWiiData();
  wiiGetter.then(function(result){
    console.log("Recieved sensor data: "+result);
  });
  newSensorData = true;
},10);
