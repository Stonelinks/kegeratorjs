var BaseModel = require('../BaseModel');
var Backbone = require('backbone');

var BeerModel = BaseModel.extend();

module.exports = Backbone.Collection.extend({
  model: BeerModel,

  parse: function(data) {
    return data.data;
  },

  url: function() {
    return BaseModel.prototype.urlRoot + '/beers/';
  }
});
