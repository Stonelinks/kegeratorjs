var Marionette = require('backbone.marionette'),
  Highcharts = require('highcharts-browserify');

Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

var LiveChart = Marionette.ItemView.extend({
    className: 'col-xs-12   ',

    template: false,

    title: undefined,

    yAxisTitle: undefined,

    seriesName: undefined,

    onShow: function(options) {
        var self = this;

        this.$el.highcharts({
            chart: {
                type: 'line',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function() {
                        Marionette.getOption(self, 'onLoad').call(self, this);
                        self.$el.find('text[text-anchor="end"]:contains(Highcharts)').hide();
                    }
                }
            },
            title: {
                text: Marionette.getOption(this, 'title')
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: Marionette.getOption(this, 'yAxisTitle')
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: Marionette.getOption(this, 'series')
            //series: [{
            //    name: Marionette.getOption(this, 'seriesName'),
                //data: (function() {
                //    // generate an array of random data
                //    var data = [],
                //        time = (new Date()).getTime(),
                //        i;
                //
                //    for (i = -100; i <= 0; i += 1) {
                //        data.push({
                //            x: time + i * 1000,
                //            y: 0.0
                //        });
                //    }
                //    return data;
                //}())
            //}]
        })
    }
});

module.exports = LiveChart;
