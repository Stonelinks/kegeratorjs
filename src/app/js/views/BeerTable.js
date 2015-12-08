var Marionette = require('backbone.marionette');

var TableView = require('./TableView');

var BeerTable = TableView.extend({

    title: 'Beer List',

    modelKeys: ['name', 'style', 'description', 'brewedBy', 'abv'],

    columnNames: {
        'name': 'Name',
        'style': 'Style',
        'description': 'Description',
        'brewedBy': 'Brewer',
        'abv': 'ABV'
    }
});

module.exports = BeerTable;
