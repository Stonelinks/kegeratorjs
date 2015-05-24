var serialPort = require('serialport');
var fs = require('fs');

var LaunchpadParser = function() {
  var newLinedelimiter = '\r\n';
  var lineDelimiter = ',';
  var encoding = 'utf8';

  var parseFloatFromSerial = function(x) {
    return parseFloat(x) * 0.001;
  };

  var data = '';
  var dataMsg = {};
  var partArray = [];
  return function(emitter, buffer) {
    data += buffer.toString(encoding);
    var parts = data.split(newLinedelimiter);
    data = parts.pop();
    parts.forEach(function(part) {
      partArray = part.split(lineDelimiter);
      if (partArray[0] == 'i') {
        emitter.emit('data', {
          raw: part,
          gyro: {
            x: parseFloatFromSerial(partArray[1]),
            y: parseFloatFromSerial(partArray[2]),
            z: parseFloatFromSerial(partArray[3])
          },
          accel: {
            x: parseFloatFromSerial(partArray[4]),
            y: parseFloatFromSerial(partArray[5]),
            z: parseFloatFromSerial(partArray[6])
          }
        });
      }
      else if (partArray[0] == 'a') {
        emitter.emit('data', {
          raw: part,
          attitude: {
            roll: parseFloat(partArray[1]) * .01,
            pitch: parseFloat(partArray[2]) * .01
          }
        });
      }
    });
  };
};

var Launchpad = function(port, baudrate) {
  port = port || '/dev/ttyS2';
  baudrate = baudrate || 115200;

  if (!fs.existsSync(port)) {
    console.log('Could not find serial port!');
    return;
  }

  this.opened = false;
  this.serial = new serialPort.SerialPort(port, {
    baudrate: baudrate,
    parser: LaunchpadParser()
  });
};

Launchpad.prototype.open = function(cb) {
  cb = cb || function() {};

  var _this = this;
  if (!this.opened) {
    this.serial.on('open', function() {
      this.opened = true;
      setTimeout(function() {
        cb.call(_this);
      }, 300);
    });
  }
  else {
    cb.call(this);
  }
};

Launchpad.prototype.write = function(s, cb) {
  cb = cb || function() {};

  var _this = this;
  var _write = function() {
    _this.serial.write(s, cb);
  };

  if (!this.opened) {
    this.open(_write);
  }
  else {
    _write();
  }
};

Launchpad.prototype.close = function(cb) {
  cb = cb || function() {};

  if (this.opened) {
    this.serial.close(cb);
    this.opened = false;
  }
  else {
    cb.call(this);
  }
};

module.exports = Launchpad;
