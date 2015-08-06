var Backbone = require('backbone');

module.exports = Backbone.Model.extend({
  urlRoot: '/api/v1',

  url: function() {
    return this.urlRoot + '/' + this.endPoint + '/';
  }
});
