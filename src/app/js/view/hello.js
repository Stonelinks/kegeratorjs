var Marionette = require('backbone.marionette');

var ConsoleView = Marionette.ItemView.extend({
  template: require('../../tmpl/hello.hbs')
});

module.exports = ConsoleView;
