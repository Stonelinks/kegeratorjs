var Marionette = require('backbone.marionette');

var LiveChart = require('../views/liveChart');

var ThermostatChart = LiveChart.extend({
  title: 'Average Temperature',
  yAxisTitle: 'Temperature (C)',
  seriesName: 'Temperature',

  onLoad: function(chart) {
    var thermostat = this.model;
    var series = chart.series[0];
    setInterval(function() {
      thermostat.fetch().done(function() {
        var x = (new Date()).getTime(), // current time
            y = parseFloat(thermostat.get('avgDegC'));
        series.addPoint([x, y], true, true);
      });
    }, 5000);
  }
});

module.exports = ThermostatChart;
