var Marionette = require('backbone.marionette');

var HighChart = require('./common/ChartView');

var ThermostatRealtimeChart = HighChart.extend({
    title: 'Temperature',
    yAxisTitle: 'Temperature (C)',

    _pollingInterval: null,

    onLoad: function () {
        var thermostat = this.model;
        var chart = this.chartInstance
        var _poll = function () {
            thermostat.fetch().done(function () {
                var x = (new Date()).getTime(), // current time
                    setPointDegC = parseFloat(thermostat.get('setPointDegC')),
                    deadBandDegC = parseFloat(thermostat.get('deadBandDegC'));

                chart.series[0].addPoint([x, parseFloat(thermostat.get('degC'))]);
                chart.series[1].addPoint([x, setPointDegC]);
                chart.series[2].addPoint([x, parseFloat(thermostat.get('avgDegC'))]);
                chart.series[3].addPoint([x, setPointDegC + deadBandDegC]);
                chart.series[4].addPoint([x, setPointDegC - deadBandDegC]);
            });
        }
        _poll()
        this._pollingInterval = setInterval(_poll, 5000);
    },

    series: [{name: 'Sensed'},
        {name: 'Commanded'},
        {name: 'Average'},
        {name: 'UpperLimit'},
        {name: 'LowerLimit'}],

    onDestroy: function () {
        clearInterval(this._pollingInterval);
    }
});

module.exports = ThermostatRealtimeChart;
