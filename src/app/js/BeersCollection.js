var BaseModel = require('./common/BaseModel');
var BaseCollection = require('./common/BaseCollection');

var BeerModel = BaseModel.extend();

module.exports = BaseCollection.extend({
  model: BeerModel,
  endPoint: 'beers'
});
