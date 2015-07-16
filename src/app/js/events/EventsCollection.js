var BaseModel = require('../BaseModel');
var BaseCollection = require('../BaseCollection');

var EventModel = BaseModel.extend();

module.exports = BaseCollection.extend({
  model: EventModel,
  endPoint: 'events'
});
