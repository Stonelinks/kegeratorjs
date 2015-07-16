var BaseModel = require('../BaseModel');
var BaseCollection = require('../BaseCollection');

var KegModel = BaseModel.extend();

module.exports = BaseCollection.extend({
  model: KegModel,
  endPoint: 'kegs'
});
