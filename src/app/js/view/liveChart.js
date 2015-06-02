var Marionette = require('backbone.marionette');
  Backbone = require('backbone'),
  smoothie = require('smoothie');

var LiveChart = Marionette.ItemView.extend({
  template: false,
  tagName: 'canvas',
  className: 'liveChart',

  initialize: function(options) {
    //this.$el.attr('width', 1200);
    this.$el.attr('height', 200);
    var chartOpts = {
          grid: {
            fillStyle: 'rgba(255,255,255,0.1)'
          }
    };
      if (options.min && options.max) {
          chartOpts.maxValue = options.max;
          chartOpts.minValue = options.min;
      }

    this.chart = new smoothie.SmoothieChart(chartOpts);

    this.series = new smoothie.TimeSeries();
        this.chart.addTimeSeries(this.series, { strokeStyle: 'rgba(192, 33, 38, 1)', lineWidth: 3 });
  },

  setWidth: function(width) {
    this.$el.attr('width', width);
  },

  onRender: function() {
    this.chart.streamTo(this.el, 500);
  },

  addPoint: function(value) {
    this.series.append(new Date().getTime(), value);
  },

  clear: function() {
    this.series.clear();
  }

});


module.exports = LiveChart;
