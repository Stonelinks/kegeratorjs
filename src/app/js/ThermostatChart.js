var Marionette = require('backbone.marionette');

var LiveChart = require('./common/LiveChartView');

var ThermostatChart = LiveChart.extend({
  title: 'Temperature',
  yAxisTitle: 'Temperature (C)',

  _pollingInterval: null,

  onLoad: function(chart) {
    var thermostat = this.model;
    this._pollingInterval = setInterval(function() {
      thermostat.fetch().done(function() {
        var x = (new Date()).getTime(), // current time
            setPointDegC = parseFloat(thermostat.get('setPointDegC')),
            deadBandDegC = parseFloat(thermostat.get('deadBandDegC'));

        chart.series[0].addPoint([x, parseFloat(thermostat.get('degC'))]);
        chart.series[1].addPoint([x, setPointDegC]);
        chart.series[2].addPoint([x, parseFloat(thermostat.get('avgDegC'))]);
        chart.series[3].addPoint([x, setPointDegC + deadBandDegC]);
        chart.series[4].addPoint([x, setPointDegC - deadBandDegC]);
      });
    }, 5000);
  },

  series: [{name: 'Sensed'},
           {name: 'Commanded'},
           {name: 'Average'},
           {name: 'UpperLimit'},
           {name: 'LowerLimit'}],

  onDestroy: function() {
    clearInterval(this._pollingInterval);
  }
});

module.exports = ThermostatChart;
