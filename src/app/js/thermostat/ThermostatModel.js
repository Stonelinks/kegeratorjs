var BaseModel = require('../BaseModel');

var ThermostatModel = BaseModel.extend({
  endPoint: 'thermostat'
});

module.exports = ThermostatModel;
