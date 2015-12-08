/**
 * Created by ldoyle on 12/7/2015.
 */

var Base = require('./Base');

var ThermostatModel = Base.Model.extend({
    endPoint: 'thermostat',

    parse: function(data) {
        return data.data;
    }
});

var ThermostatCollection = Base.Collection.extend({
    model: ThermostatModel
});

module.exports = {
    Model: ThermostatModel,
    Collection: ThermostatCollection
};
