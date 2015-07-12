var Marionette = require('backbone.marionette');

var BeersCollection = require('./BeersCollection');

var TableView = require('../views/table');
var RowView = require('../views/row');

var BeerPage = RowView.extend({
  childView: TableView
})

module.exports = function(viewPort) {
  var beerCollection = new BeersCollection();
  beerCollection
    .fetch()
    .then(function() {

      viewPort.show(new BeerPage({
        collection: beerCollection
      }));
    });
};
