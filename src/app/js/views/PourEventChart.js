/**
 * Created by ld on 8/6/15.
 */
var Marionette = require('backbone.marionette');
var moment = require('moment');
var _ = require('underscore');
var HighChart = require('./ChartView');

var PourEventChart = HighChart.extend({
    title: 'Pour History',
    yAxisTitle: 'Volume (L)',

    series: function() {

        var series = ['Pours'].map(function(seriesName) {
            return {
                name: seriesName,
                data: []
            };
        });

        var pourEvents = this.collection.where({
            type: 'pouredBeer'
        });

        pourEvents.forEach(function(event) {
            var x = event.get('time') * 1000;
            series[0].data.push([x, parseFloat(event.get('data').volumeL)]);
        });

        return series;
    },

    onDestroy: function() {
    }
});

module.exports = PourEventChart;
