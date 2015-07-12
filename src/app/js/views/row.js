var Marionette = require('backbone.marionette');

module.exports = Marionette.LayoutView.extend({
  template: require('../../tmpl/row.hbs'),

  regions: {
    row: ".row:first-of-type"
  },
  
  onShow: function() {
    if (this.childView) {
      this.getRegion('row').show(new this.childView(this.options))
    }
  }
});
