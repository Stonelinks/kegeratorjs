var Marionette = require('backbone.marionette');

module.exports = Marionette.LayoutView.extend({
  template: require('../../tmpl/row.hbs'),

  childViews: [],

  initialize: function() {
    this.childViews.forEach(function(View, index) {
      this.addRegion('row' + index, '.row:nth-of-type(' + (index + 1) + ')');
    }.bind(this));
  },

  templateHelpers: function() {
    return {
      childViews: this.childViews
    };
  },

  onShow: function() {
    this.childViews.forEach(function(View, index) {
      this.getRegion('row' + index).show(new View(this.options));
    }.bind(this));
  }
});
