var Marionette = require('backbone.marionette');

var BeersCollection = require('./BeersCollection')

module.exports = Marionette.ItemView.extend({
  template: function() {
    return '<center><h1>Some shit about beer:</h1></center><pre>' + '' + '</pre>';
  },
  
  initialize: function() {
    this.bc = new BeersCollection()
    this.bc.fetch();
  }
})
