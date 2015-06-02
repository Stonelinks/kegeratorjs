var Marionette = require('backbone.marionette');
var LiveChart = require('./liveChart');

var SensorDataView = Marionette.ItemView.extend({
  template: require('../../tmpl/sensordata.hbs'),
  
  initialize: function() {
    setInterval(function() {
      this.model.fetch();
    }.bind(this), 500)
  },
  
  modelEvents: {
    'change': function() {
      if (this.thermostatChart) {
        this.thermostatChart.addPoint(this.model.get('thermostat'))
      }
    }
  },

  onRender: function() {

    // charts
    this.thermostatChart = new LiveChart({
      min: 0,
      max: 100.0
    }).render()
    this.$el.find("#kegerator-strips").append(this.thermostatChart.$el);

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

module.exports = SensorDataView;
