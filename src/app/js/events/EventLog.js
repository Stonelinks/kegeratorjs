var Marionette = require('backbone.marionette');
var moment = require('moment');

var util = require('../util');

var EventItem = Marionette.ItemView.extend({
  template: require('../../tmpl/eventitem.hbs'),

  templateHelpers: function() {
    var time = moment(this.model.get('time')*1000);
    return {
      eventType: util.camelCaseToRegularForm(this.model.get('type')),
      dataJSON: JSON.stringify(this.model.get('data'), null, 4),
      time: time.format('MMMM Do YYYY, h:mm:ss a'),
      timeFromNow: time.fromNow()
    };
  }
});

module.exports = Marionette.CollectionView.extend({
  childView: EventItem
});
