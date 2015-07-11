var Marionette = require('backbone.marionette');

var BeersCollection = require('./BeersCollection');

var TableView = require('../views/table');

var BeerView = Marionette.ItemView.extend({
  template: require('../../tmpl/beer.hbs')
});

var BeersView = Marionette.CollectionView.extend({
  childView: BeerView
});

module.exports = function(viewPort) {
  var beerCollection = new BeersCollection();
  beerCollection
    .fetch()
    .then(function() {
      viewPort.show(new TableView({
        collection: beerCollection
      }));
    });
};
