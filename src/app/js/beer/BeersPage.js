var Marionette = require('backbone.marionette');

var BeersCollection = require('./BeersCollection');

var BeerView = Marionette.ItemView.extend({
  template: function() {
    return '<center><h1>Some shit about beer:</h1></center><pre>' + '' + '</pre>';
  },

  initialize: function() {
    debugger;
  }
});


module.exports = function(viewPort) {
  var beerCollection = new BeersCollection();
  beerCollection.fetch().then(function() {
    debugger;
    viewPort.show(new BeerView({
      collection: beerCollection
    }));
  });
};
