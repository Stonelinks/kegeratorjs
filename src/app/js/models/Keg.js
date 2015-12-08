/**
 * Created by ldoyle on 12/7/2015.
 */


var Base = require('./Base');

var KegModel = Base.Model.extend();

var KegCollection = Base.Collection.extend({
    model: KegModel,
    endPoint: 'kegs'
});

module.exports = {
    Model: KegModel,
    Collection: KegCollection
};
