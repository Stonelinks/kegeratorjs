var BaseModel = require('./common/BaseModel');
var BaseCollection = require('./common/BaseCollection');

var KegModel = BaseModel.extend();

module.exports = BaseCollection.extend({
    model: KegModel,
    endPoint: 'kegs'
});
