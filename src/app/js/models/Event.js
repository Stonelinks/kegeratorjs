/**
 * Created by ldoyle on 12/7/2015.
 */


var Base = require('./Base');

var EventModel = Base.Model.extend();

var EventCollection = Base.Collection.extend({
    model: EventModel,
    endPoint: 'events',
    comparator: 'time'
});

module.exports = {
    Model: EventModel,
    Collection: EventCollection
};
