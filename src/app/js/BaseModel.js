var Backbone = require('backbone');

module.exports = Backbone.Model.extend({
  urlRoot: '/api/v1',

  parse: function(data) {
    return data.data;
  },

  url: function() {
    return this.urlRoot + '/' + this.endPoint + '/';
  }
});
