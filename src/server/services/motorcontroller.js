// closed loop motor controller
// from an attitude estimate and command, uses PID control to send motor commands

var PIDController = require('./PIDController')

var satf = function(input, min, max) {
  return Math.floor(Math.min(max, Math.max(min, parseInt(input))))
}

var radiansTo255 = function(input) {
  return Math.floor(127 + (input * 2.0 * 127 / Math.PI))
}

var MotorController = function() {
  this.rollGains = {}
  this.pitchGains = {}
  this.yawRange = 0.0
  this.dt = 0.0
};

MotorController.prototype.start = function() {
  this.yawScale = 
  this.rollController = new PIDController(this.rollGains)
  this.pitchController = new PIDController(this.pitchGains)
}

MotorController.prototype.getMotorOutput = function(attitudeEstimate, commands) {

  this.rollController.setTarget(commands.roll)
  this.pitchController.setTarget(commands.pitch)
  
  var roll = satf(this.rollController.update(radiansTo255(attitudeEstimate.roll)), 0, 254)
  var pitch = satf(this.pitchController.update(radiansTo255(attitudeEstimate.pitch)), 0, 254)
  
  var throttle = 0//commands.throttle
  var yaw = satf(Math.floor(127 + satf(commands.yaw * 127 / this.yawRange, -radiansTo255(this.yawRange), radiansTo255(this.yawRange))), 0, 254)
  console.log({
    yaw: yaw,
    pitch: pitch,
    roll: roll
  })

  return {
    m1: satf(throttle - pitch + roll - yaw, 0, 254),
    m2: satf(throttle + pitch - roll - yaw,  0, 254),
    m3: satf(throttle + pitch + roll + yaw, 0, 254),
    m4: satf(throttle - pitch - roll + yaw,  0, 254)
  }
}

module.exports = MotorController;
