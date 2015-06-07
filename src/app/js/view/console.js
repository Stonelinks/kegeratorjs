var Marionette = require('backbone.marionette');
var LogView = require('./log');
var ThreeDSliderView = require('./3dSlider');
var LiveChart = require('./liveChart');
var AttitudeView = require('./attitude');

var ConsoleView = Marionette.ItemView.extend({
  template: require('../../tmpl/console.hbs'),

  onRender: function() {
      $('#myTab a:last').tab('show');

    this.logView = new LogView();
    this.logView.render();
    this.$el.find('#log').html(this.logView.$el);


    var attitudeModel = new Backbone.Model({
      roll: 0,
      pitch: 0
    });
    var attitude = new AttitudeView({
      el: this.$el.find('#attitude'),
      model: attitudeModel
    });
    attitude.render();

/*
    var gyroSlider = new ThreeDSliderView({
      model: gyroModel
    });
    gyroSlider.render();
    this.$el.find("#gyro").html(gyroSlider.$el);
*/
    // gyrocharts
    var gyroModel = new Backbone.Model({
      value: {
        x: 0,
        y: 0,
        z: 0
      },
      step: 0.001,
      max: Math.PI,
      min: -Math.PI
    });

    var gyroChartOptions = {
      min: -Math.PI,
      max: Math.PI
    };

    var gyroCharts = {
      x: new LiveChart(gyroChartOptions),
      y: new LiveChart(gyroChartOptions),
      z: new LiveChart(gyroChartOptions)
    };
    var width = this.$el.find('#chart-holder').width() - 45;
    for (var axis in gyroCharts) {
      gyroCharts[axis].render();
      gyroCharts[axis].setWidth(width - 45);
      this.$el.find('#gyro-strips').append(gyroCharts[axis].$el);
    }

    this.$el.on('shown.bs.tab', function() {
      var width = this.$el.find('#chart-holder').width() - 45;
      console.log('showing with width of: %s', width);
      for (var axis in gyroCharts) {
        gyroCharts[axis].setWidth(width - 45);
      }
    }.bind(this));
    $(window).resize(function(e) {
      var width = this.$el.find('#chart-holder').width() - 45;
      for (var axis in gyroCharts) {
        gyroCharts[axis].setWidth(width - 45);
      }
    }.bind(this));

    var selectedStrip = 'gyro';
    this.$el.find('#strip-selector').change(function(e) {
      selectedStrip = e.target.value.toLowerCase();
      for (var axis in gyroCharts) {
        gyroCharts[axis].clear();
      }
    });


    // accel charts
    /*
    var accelChartOptions = {
      min: -10,
      max: 10
    };
    var accelCharts = {
      x: new LiveChart(accelChartOptions),
      y: new LiveChart(accelChartOptions),
      z: new LiveChart(accelChartOptions)
    };
    for (var axis in accelCharts) {
      accelCharts[axis].render();
      this.$el.find('#accel-strips').append(accelCharts[axis].$el);
    }

    // attitude charts
    var attitudeChartOptions = {
      min: -Math.PI / 2,
      max: Math.PI / 2
    };
    var attitudeCharts = {
      roll: new LiveChart(attitudeChartOptions),
      pitch: new LiveChart(attitudeChartOptions)
    };
    for (var axis in attitudeCharts) {
      attitudeCharts[axis].render();
      this.$el.find('#attitude-strips').append(attitudeCharts[axis].$el);
    }

    // launchpad debug charts
    var launchpadDebugCharts = {
      delay: new LiveChart({
        min: 0,
        max: 10000
      })
    }
    for (var axis in launchpadDebugCharts) {
      launchpadDebugCharts[axis].render();
      this.$el.find("#launchpad-debug-strips").append(launchpadDebugCharts[axis].$el);
    }
*/
    // var client = require('mqtt').connect();
    // client.subscribe('vehicle/sensor/+');
    // client.subscribe('vehicle/attitude');
//
    // client.on('message', function(topic, payload) {
      // if (topic === "vehicle/sensor/gyro" && selectedStrip === 'gyro') {
        // var data = JSON.parse(payload.toString());
        // gyroCharts.x.addPoint(data.x);
        // gyroCharts.y.addPoint(data.y);
        // gyroCharts.z.addPoint(data.z);
      // }
      // if (topic === "vehicle/sensor/accel" && selectedStrip === 'accel') {
        // var data = JSON.parse(payload.toString());
        // gyroCharts.x.addPoint(data.x);
        // gyroCharts.y.addPoint(data.y);
        // gyroCharts.z.addPoint(data.z);
      // }
      // if (topic === "vehicle/attitude") {
        // var data = JSON.parse(payload.toString());
        // attitudeModel.set(data);
        // gyroCharts.x.addPoint(data.pitch);
        // gyroCharts.z.addPoint(data.roll);
      // }
    // });
  }

});

module.exports = ConsoleView;
