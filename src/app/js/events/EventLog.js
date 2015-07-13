var Marionette = require('backbone.marionette');

var util = require('../util');

var EventItem = Marionette.ItemView.extend({
  template: require('../../tmpl/eventitem.hbs'),

  templateHelpers: function() {
    return {
      eventType: util.camelCaseToRegularForm(this.model.get('type')),
      dataJSON: JSON.stringify(this.model.get('data'), null, 4)
    };
  }
});

module.exports = Marionette.CollectionView.extend({
  childView: EventItem
});
