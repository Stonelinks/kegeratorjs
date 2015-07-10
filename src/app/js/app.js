var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
Backbone.$ = window.$ = window.jQuery = $;
var Marionette = require('backbone.marionette');
require('bootstrap');

var app = new Marionette.Application();
window.app = app;

app.addRegions({
  nav: '#nav',
  content: '#content'
});

// set up nav
var Nav = require('./nav');
var nav = new Nav();
app.addInitializer(function(opts) {
  app.getRegion('nav').show(nav);
  nav.selectActiveButton();
});

// main pages
var showView = function(viewWrapperFunc) {
  return function() {
    var viewPort = app.getRegion('content');
    viewWrapperFunc(viewPort);
  }
};

var createDummyView = function(msg) {
  var DummyView = Marionette.ItemView.extend({
    template: function() {
      console.log(msg);
      return '<center><h1>' + msg + '</h1></center>';
    }
  });
  return showView(function(viewPort) {
    viewPort.show(new DummyView());
  });
};

var pages = {
  dashboard: createDummyView('Nothing here yet'),
  beers: showView(require('./beer/BeersPage')),
  sensors: createDummyView('I\'m the sensor page'),
  settings: createDummyView('I\'m the settings page')
};
pages['*catchall'] = pages.dashboard;

var Router = Marionette.AppRouter.extend({
  routes: pages
});

// start the router
app.addInitializer(function(opts) {
  this.router = new Router();
  this.router.on('route', function() {
    nav.selectActiveButton();
  });
  Backbone.history.start({
    // pushState: true
  });
});

app.start();
