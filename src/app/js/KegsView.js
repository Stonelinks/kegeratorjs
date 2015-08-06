var Marionette = require('backbone.marionette');
var util = require('./util');
var _ = require('underscore');

var KegView = Marionette.ItemView.extend({
    template: require('../tmpl/keg.hbs'),

    templateHelpers: function() {
        var beer = this.model.get('beer');
        this.model.set('consumedP', parseInt(util.literToPints(this.model.get('consumedL'))));
        this.model.set('capacityP', parseInt(util.literToPints(this.model.get('capacityL'))));
        return {
            kegName: 'Keg ' + (parseInt(this.model.get('id')) + 1),
            beer: beer.toJSON(),
            keg: _.mapObject(this.model.toJSON(), function(field) {
                return _.isNumber(field) ? parseInt(field) : field;
            }),
            percentConsumed: parseInt(100.0 - parseFloat(this.model.get('consumedL')) / parseFloat(this.model.get('capacityL')) * 100.0),
            remainingL: parseInt(parseFloat(this.model.get('capacityL')) - parseFloat(this.model.get('consumedL'))),
            remainingPints: parseInt(util.literToPints(parseFloat(this.model.get('capacityL')) - parseFloat(this.model.get('consumedL'))))
            //dataJSON: JSON.stringify(this.model.get('data'), null, 4),
            //time: time.format('MMMM Do YYYY, h:mm:ss a'),
            //timeFromNow: time.fromNow()
        };
    }
});

module.exports = Marionette.CollectionView.extend({
    childView: KegView
});
