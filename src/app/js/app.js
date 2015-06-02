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
    '*catchall' : 'showGreeter',
    // 'controls' : 'showControls'
  },

  showGreeter: function() {
    var greeterView = require('./view/hello');
    app.getRegion('content').show(new greeterView());
  },

  showConsole: function() {
    // var ConsoleView = require('./view/console');
    // app.getRegion('content').show(new ConsoleView());
  },

  showControls: function() {
    // var ControlsView = require('./view/controls');
    // app.getRegion('content').show(new ControlsView());
  }
});

// start the router
app.addInitializer(function(opts) {
  this.router = new Router();
  Backbone.history.start({pushState: true});
});

app.start();
