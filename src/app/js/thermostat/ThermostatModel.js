var BaseModel = require('../BaseModel');

var ThermostatModel = BaseModel.extend({
  endPoint: 'thermostat',

  parse: function(data) {
    return data.data;
  }
});

module.exports = ThermostatModel;
