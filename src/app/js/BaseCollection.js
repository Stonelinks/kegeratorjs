var BaseModel = require('./BaseModel');
var Backbone = require('backbone');

module.exports = Backbone.Collection.extend({
  parse: function(data) {
    return data.data;
  },

  url: function() {
    return BaseModel.prototype.urlRoot + '/' + this.endPoint + '/';
  }
});
