var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
Backbone.$ = window.$ = window.jQuery = $;
var Marionette = require('backbone.marionette');
var Pages = require('./Pages');
require('bootstrap');

var app = new Marionette.Application();
window.app = app;

app.addRegions({
    nav: '#nav',
    content: '#content'
});

// set up nav
var Nav = require('./NavView');
var nav = new Nav();
app.addInitializer(function () {
    app.getRegion('nav').show(nav);
});

// main pages
var showView = function (viewWrapperFunc) {
    return function () {
        var viewPort = app.getRegion('content');
        viewWrapperFunc(viewPort);
    }
};

var pages = {
    realtime: showView(Pages.realtime),
    kegs: showView(Pages.kegs),
    history: showView(Pages.history)
};
pages['*catchall'] = pages.dashboard;

var Router = Marionette.AppRouter.extend({
    routes: pages
});

// start the router
app.addInitializer(function (opts) {
    this.router = new Router();
    this.router.on('route', function () {
        nav.render();
    });
    Backbone.history.start({
        // pushState: true
    });
});

app.start();
