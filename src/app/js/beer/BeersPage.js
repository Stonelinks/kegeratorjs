var Marionette = require('backbone.marionette');

var BeersCollection = require('./BeersCollection');

var TableView = require('../views/table');
var RowView = require('../views/row');

var BeerTable = TableView.extend({
  modelKeys: ['name', 'style', 'description', 'brewedBy', 'abv'],

  columnNames: {
    'name': 'Name',
    'style': 'Style',
    'description': 'Description',
    'brewedBy': 'Brewer',
    'abv': 'ABV'
  }
});

var BeerPage = RowView.extend({
  childView: BeerTable
});

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
