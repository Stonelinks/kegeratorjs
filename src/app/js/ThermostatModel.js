var BaseModel = require('./common/BaseModel');

var ThermostatModel = BaseModel.extend({
    endPoint: 'thermostat',

    parse: function (data) {
        return data.data;
    }
});

module.exports = ThermostatModel;
