var Marionette = require('backbone.marionette');

var TableView = require('../views/table');

var BeersTable = TableView.extend({
  
  modelKeys: ['name', 'style', 'description', 'brewedBy', 'abv'],

  columnNames: {
    'name': 'Name',
    'style': 'Style',
    'description': 'Description',
    'brewedBy': 'Brewer',
    'abv': 'ABV'
  }
});

module.exports = BeersTable
