var Marionette = require('backbone.marionette');

var BeersCollection = require('./beer/BeersCollection');
var KegsCollection = require('./keg/KegsCollection');

var BeersTable = require('./beer/BeersTable')
var KegsTable = require('./keg/KegsTable')

var RowView = require('./views/row');

var BeerPage = RowView.extend({
  childView: BeersTable
});

module.exports = function(viewPort) {
  var kegs = new KegsCollection();
  var beers = new BeersCollection();
  
  kegs
    .fetch()
    .then(function() {
      beers
        .fetch()
        .then(function() {
          viewPort.show(new BeerPage({
            collection: beers
          }));
        });
    });
};
