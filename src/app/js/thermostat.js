var Marionette = require('backbone.marionette');

var ThermostatModel = require('./thermostat/ThermostatModel');

var ThermostatChart = require('./thermostat/ThermostatChart');

var RowView = require('./views/row');


module.exports = function(viewPort) {
  var thermostat = new ThermostatModel();

  thermostat
    .fetch()
    .then(function() {

        var ThermostatPage = RowView.extend({
          childViews: [
            ThermostatChart.extend({
              model: thermostat
            })
          ]
        });

        viewPort.show(new ThermostatPage());
      });
};
