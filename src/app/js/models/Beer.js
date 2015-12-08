/**
 * Created by ldoyle on 12/7/2015.
 */


var Base = require('./Base');

var BeerModel = Base.Model.extend();

var BeerCollection = Base.Collection.extend({
    model: BeerModel,
    endPoint: 'beers'
});

module.exports = {
    Model: BeerModel,
    Collection: BeerCollection
};
