var Marionette = require('backbone.marionette');

var EventsCollection = require('./events/EventsCollection');

var EventLog = require('./events/EventLog');

var RowView = require('./views/row');

module.exports = function(viewPort) {
  var events = new EventsCollection();

  events
    .fetch()
    .then(function() {
      var EventsPage = RowView.extend({
        childViews: [
          EventLog.extend({
            collection: events
          })
        ]
      });

      viewPort.show(new EventsPage());
    });
};
