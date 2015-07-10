var Marionette = require('backbone.marionette');

var RowView = Marionette.ItemView.extend({
  tagName: "tr",
  template: require('../../tmpl/tablerow.hbs'),
  
  templateHelpers: function() {
    return {
      sortedModelKeys: this.model.keys().sort()
    };
  }
});

module.exports = Marionette.CompositeView.extend({
  childView: RowView,

  childViewContainer: "tbody",

  template: require('../../tmpl/table.hbs')
});
