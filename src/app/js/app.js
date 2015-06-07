var $ = require('jquery');
var Backbone = require('backbone');
Backbone.$ = window.$ = window.jQuery = $;
var Marionette = require('backbone.marionette');
require('bootstrap');

var Nav = require('./view/nav');

var createDummyview = function(msg) {
  return Marionette.ItemView.extend({
    template: function() {
      console.log(msg);
      return '<h1>' + msg + '</h1>';
    }
  });
};

var pages = {
  dashboard: createDummyview('I\'m the dashboard page'),
  sensors: createDummyview('I\'m the sensor page'),
  settings: createDummyview('I\'m the settings page')
};

var app = new Marionette.Application();
window.app = app;

app.addRegions({
  nav: '#nav',
  content: '#content'
});


// set up nav
var nav = new Nav()
app.addInitializer(function(opts) {
  app.getRegion('nav').show(nav);
  nav.selectActiveButton();
});

var Router = Marionette.AppRouter.extend({

  routes: {
    'dashboard' : 'showDashboard',
    'sensors' : 'showSensors',
    'settings' : 'showSettings',
    '*catchall' : 'showDashboard'
  },

  showDashboard: function() {
    app.getRegion('content').show(new pages.dashboard());
  },

  showSettings: function() {
    app.getRegion('content').show(new pages.settings());
  },

  showSensors: function() {
    app.getRegion('content').show(new pages.sensors());
  },

  showSensorData: function() {
    var SensorDataView = require('./view/sensordata');

    var SensorDataModel = Backbone.Model.extend({
      url: function() {
        return '/sensor_data';
      }
    });

    app.getRegion('content').show(new SensorDataView({
      model: new SensorDataModel()
    }));
  }
});

// start the router
app.addInitializer(function(opts) {
  this.router = new Router();
  this.router.on('route', function() {
    nav.selectActiveButton();
  })
  Backbone.history.start({
    // pushState: true
  });
});

app.start();
