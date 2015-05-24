var mqtt    = require('mqtt');
var client  = mqtt.connect('mqtt://localhost:1883');
client.publish('vehicle/sensor/gyro', {x: Math.random(), y: Math.random(), z: Math.random()});
client.end();
