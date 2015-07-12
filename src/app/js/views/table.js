var Marionette = require('backbone.marionette');
var _ = require('underscore');

var templateHelpers = function() {

  var modelKeys = [];
  if (Marionette.getOption(this, 'modelKeys')) {
    modelKeys = Marionette.getOption(this, 'modelKeys');
  } else if (this.model || (this.collection && this.collection.at(0))) {
    var model = this.model ? this.model : this.collection.at(0);
    modelKeys = model.keys().sort();
  }

  return {
    modelKeys: modelKeys,
    modelKeysUpperCase: modelKeys.map(function(key) {
      return key.toUpperCase();
    })
  };
};

var TableRowView = Marionette.ItemView.extend({
  tagName: 'tr',

  template: require('../../tmpl/tablerow.hbs'),

  templateHelpers: function() {
    var helpers = templateHelpers.call(this);
    return _.extend(helpers, {
      model: this.model,
      modelValues: helpers.modelKeys.map(function(key) {
        return this.model.get(key);
      }.bind(this))
    });
  }
});

module.exports = Marionette.CompositeView.extend({
  childView: TableRowView,

  childViewContainer: 'tbody',

  template: require('../../tmpl/table.hbs'),

  templateHelpers: templateHelpers,

  childViewOptions: function() {
    return {
      modelKeys: Marionette.getOption(this, 'modelKeys')
    };
  }
});
