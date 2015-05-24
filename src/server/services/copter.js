var Launchpad = require('./launchpad');
var MotorController = require('./motorcontroller');
var mqtt = require('mqtt');
var _ = require('lodash');

var forceUseFakeData = false;

var timing = {
  sensorThrottle: 50,
  attitudeThrottle: 50,
  fakeDataInterval: 250,
  controlsLogInterval: 500,
  motorLogInterval: 500,
  writerInterval: 20,
  motorControllerInterval: 20
};

var motorControllerGains = {
  k_p: 1.0,
  k_i: .1,
  k_d: 0
};

function kegeratorService() {
  this.controlInput = {
    yaw: 127,
    pitch: 127,
    roll: 127,
    throttle: 127
  };
  this.gyro = {
    x: 0,
    y: 0,
    z: 0
  };
  this.accel = {
    x: 0,
    y: 0,
    z: 0
  };
  this.attitude = {
    roll: 0,
    pitch: 0
  };
  this.motorOutput = {
    m1: 127,
    m2: 127,
    m3: 127,
    m4: 127
  }
}

kegeratorService.prototype.start = function() {

  this.client = this.setupMqtt({
		'vehicle/controls': this.updateControls.bind(this)
  });

  this.startControlsLog();

	this.launchpad = new Launchpad();

  this.motorController = new MotorController()
  this.motorController.pitchGains = motorControllerGains
  this.motorController.rollGains = motorControllerGains
  this.motorController.yawRange = Math.PI / 6.0
  this.motorController.dt = timing.motorControllerInterval

	if (this.launchpad.serial && !forceUseFakeData) {
    this.startLaunchpadListener();
    this.startMotorController()
    this.startLaunchpadWriter();
  }
 else {
   this.startGenerateFakeData();
  }

  console.log('started kegerator service');
};

kegeratorService.prototype.setupMqtt = function(topics) {
	console.log('setting up mqtt');
	var client = mqtt.connect('mqtt://localhost:1883');

	for (var topic in topics) {
		client.subscribe(topic);
	}
	client.publish('vehicle/sensor/accel', {x: Math.random(), y: Math.random(), z: Math.random()});

  client.on('message', function(topic, payload) {
    if (topics[topic]) {
      var data;
      try {
        data = JSON.parse(payload.toString());
      } catch (e) {
        data = payload.toString();
      }
      topics[topic].call(this, data);
    }
	}.bind(this));

	return client;
};

kegeratorService.prototype.updateControls = function(controls) {
  var mapControlToRange = function(input) {
    return Math.max(0, Math.min(255, Math.floor(127 + (input * 127))));
  };

  for (thing in controls) {
    this.controlInput[thing] = mapControlToRange(controls[thing]);
  }
};

kegeratorService.prototype.publish = function(data) {
  for (topic in data) {
    if (data[topic]) {
      this.client.publish(topic, JSON.stringify(data[topic]));
    }
  }
};

kegeratorService.prototype.onSensorData = function(data) {
  this.gyro = data.gyro
  this.accel = data.accel
  this.publishSensorData()
}

kegeratorService.prototype.onAttitudeData = function(data) {
  this.attitude = data.attitude
  this.publishAttitudeData()
}

kegeratorService.prototype.publishSensorData = _.throttle(function() {
  this.publish({
    'vehicle/sensor/gyro': this.gyro,
    'vehicle/sensor/accel': this.accel
  });
}, timing.sensorThrottle);

kegeratorService.prototype.publishAttitudeData = _.throttle(function() {
  this.publish({
    'vehicle/attitude': this.attitude
  });
}, timing.attitudeThrottle);

kegeratorService.prototype.startControlsLog = function() {
  setInterval(function() {
    console.log(this.controlInput);
    this.publish({
    	'vehicle/log/trace' : this.controlInput
    })
  }.bind(this), timing.controlsLogInterval);
};

kegeratorService.prototype.startMotorLog = function() {
  setInterval(function() {
    console.log(this.controlInput);
    this.publish({
    	'vehicle/log/trace' : this.controlInput
    })
  }.bind(this), timing.controlsLogInterval);
};

kegeratorService.prototype.startLaunchpadListener = function() {
  this.launchpad.serial.on('data', function(data) {
    if (data.hasOwnProperty('gyro') && data.hasOwnProperty('accel')) {
      this.onSensorData.call(this, data);
    }
    if (data.hasOwnProperty('attitude')) {
      this.onAttitudeData.call(this, data);
    }
  }.bind(this));
};

kegeratorService.prototype.startLaunchpadWriter = function() {
  setInterval(function() {
    this.launchpad.serial.write(new Buffer([255, parseInt(this.controlInput.roll), parseInt(this.controlInput.pitch), parseInt(this.controlInput.yaw)]));
    // this.launchpad.serial.write(new Buffer([255, parseInt(this.motorOutput.m1), parseInt(this.motorOutput.m2), parseInt(this.motorOutput.m3), parseInt(this.motorOutput.m4)]));
  }.bind(this), timing.writerInterval);
};

kegeratorService.prototype.startMotorController = function() {
  this.motorController.start()
  setInterval(function() {
    this.motorOutput = this.motorController.getMotorOutput(this.attitude, this.controlInput)
  }.bind(this), timing.motorControllerInterval);
};

kegeratorService.prototype.startGenerateFakeData = function() {
  var t = 0
  
  setInterval(function() {
    t++
    var fakeData = {
      raw: 'raw data',
      gyro: {
        x: Math.random(),
        y: Math.random(),
        z: Math.random()
      },
      accel: {
        x: Math.random(),
        y: Math.random(),
        z: Math.random()
      },
      attitude: {
        roll: Math.sin(0.5 * t),
        pitch: Math.cos(0.5 * t)
      }
    };

    console.log('sending fake data to browser');
    this.onSensorData.call(this, fakeData);
    this.onAttitudeData.call(this, fakeData);
  }.bind(this), timing.fakeDataInterval);
};

module.exports = kegeratorService;
