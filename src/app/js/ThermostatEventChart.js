/**
 * Created by ld on 8/6/15.
 */
var Marionette = require('backbone.marionette');
var moment = require('moment');
var _ = require('underscore');
var HighChart = require('./common/ChartView');

var ThermostatEventChart = HighChart.extend({
    title: 'Temperature History',
    yAxisTitle: 'Temperature (C)',

    series: function() {

        var series = ['Sensed', 'Commanded', 'Average', 'UpperLimit', 'LowerLimit'].map(function(seriesName) {
            return {
                name: seriesName,
                data: []
            };
        });

        var thermostat = this.model;
        var temperatureEvents = this.collection.where({
            type: 'thermostatSense'
        });

        temperatureEvents.forEach(function(event) {
            var x = event.get('time') * 1000,
                setPointDegC = parseFloat(thermostat.get('setPointDegC')),
                deadBandDegC = parseFloat(thermostat.get('deadBandDegC'));

            series[0].data.push([x, parseFloat(event.get('data').degC)]);
            series[1].data.push([x, setPointDegC]);
            series[2].data.push([x, parseFloat(event.get('data').avgDegC)]);
            series[3].data.push([x, setPointDegC + deadBandDegC]);
            series[4].data.push([x, setPointDegC - deadBandDegC]);
        });

        return series;
    },

    onDestroy: function() {
    }
});

module.exports = ThermostatEventChart;
