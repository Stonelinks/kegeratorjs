var BaseModel = require('./common/BaseModel');
var BaseCollection = require('./common/BaseCollection');

var EventModel = BaseModel.extend();

module.exports = BaseCollection.extend({
    model: EventModel,
    endPoint: 'events',
    comparator: 'time'
});
