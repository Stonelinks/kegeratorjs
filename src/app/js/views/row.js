var Marionette = require('backbone.marionette');

module.exports = Marionette.CompositeView.extend({
  template: require('../../tmpl/row.hbs'),

  childViewContainer: ".row:first-of-type",
});
