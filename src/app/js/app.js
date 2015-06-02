var $ = require('jquery');
var Backbone = require('backbone');
Backbone.$ = window.$ = window.jQuery = $;
var Marionette = require('backbone.marionette');
require('bootstrap');

var app = new Marionette.Application();
window.app = app;

app.addRegions({
  content: '#content'
});

var Router = Marionette.AppRouter.extend({

  routes: {
    'sensors' : 'showSensorData',
    '*catchall' : 'showGreeter'
  },

  showGreeter: function() {
    var greeterView = require('./view/hello');
    app.getRegion('content').show(new greeterView());
  },

  showSensorData: function() {
    var SensorDataView = require('./view/sensordata');
    
    var SensorDataModel = Backbone.Model.extend({
      url: function() {
        return '/sensor_data'
      }
    });
    
    app.getRegion('content').show(new SensorDataView({
      model: new SensorDataModel()
    }));
  },
});

// start the router
app.addInitializer(function(opts) {
  this.router = new Router();
  Backbone.history.start({
    // pushState: true
  });
});

app.start();
