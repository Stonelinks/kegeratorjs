var BaseModel = require('../BaseModel');
var BaseCollection = require('../BaseCollection');

var BeerModel = BaseModel.extend();

module.exports =  BaseCollection.extend({
  model: BeerModel,
  endPoint: 'beers'
});
