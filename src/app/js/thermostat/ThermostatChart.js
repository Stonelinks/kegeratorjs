var Marionette = require('backbone.marionette');

var LiveChart = require('../views/liveChart');

var ThermostatChart = LiveChart.extend({
  title: 'Temperature',
  yAxisTitle: 'Temperature (C)',

  _pollingInterval: null,

  onLoad: function(chart) {
    var thermostat = this.model;
    var series = chart.series[0];
    var series2 = chart.series[1];
    this._pollingInterval = setInterval(function() {
      thermostat.fetch().done(function() {
        var x = (new Date()).getTime(), // current time
            y = parseFloat(thermostat.get('degC')),
            y2 = parseFloat(thermostat.get('setPointDegC'));
        //series.addPoint([x, y], true, true);
        series.addPoint([x, y]);
        series2.addPoint([x, y2]);
      });
    }, 5000);
  },

  series: [{
    name: 'Sensed temperature'
  }, {
    name: 'Commanded temperature'
  }],

  onDestroy: function() {
    clearInterval(this._pollingInterval);
  }
});

module.exports = ThermostatChart;
