var Marionette = require('backbone.marionette');

var RowView = Marionette.ItemView.extend({
  tagName: "tr",
  
  template: require('../../tmpl/tablerow.hbs'),
  
  templateHelpers: function() {
    var sortedModelKeys = this.model.keys().sort()
    var sortedModelValues = sortedModelKeys.map(function(key) {
      return this.model.get(key)
    }.bind(this))
    return {
      model: this.model,
      sortedModelValues: sortedModelValues
    };
  }
});

module.exports = Marionette.CompositeView.extend({
  childView: RowView,

  childViewContainer: "tbody",

  template: require('../../tmpl/table.hbs'),
  
  templateHelpers: function() {
    
    var sortedModelKeys = this.collection && this.collection.at(0) ? this.collection.at(0).keys().sort() : []
      
    return {
      sortedModelKeys: sortedModelKeys
    };
  }
});
