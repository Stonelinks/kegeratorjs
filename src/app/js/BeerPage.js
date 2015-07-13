var Marionette = require('backbone.marionette');

var BeersCollection = require('./beer/BeersCollection');
var KegsCollection = require('./keg/KegsCollection');

var BeersTable = require('./beer/BeersTable')
var KegsTable = require('./keg/KegsTable')

var RowView = require('./views/row');


module.exports = function(viewPort) {
  var kegs = new KegsCollection();
  var beers = new BeersCollection();
  
  kegs
    .fetch()
    .then(function() {
      beers
        .fetch()
        .then(function() {

          var BeerPage = RowView.extend({
            childViews: [
              KegsTable.extend({
                collection: kegs
              }),
              BeersTable.extend({
                collection: beers
              })
            ]
          });

          viewPort.show(new BeerPage());
        });
    });
};
