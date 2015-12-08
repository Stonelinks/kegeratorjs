/**
 * Created by ldoyle on 12/7/2015.
 */
var Backbone = require('backbone');

var BaseModel = Backbone.Model.extend({
    urlRoot: '/api/v1',

    url: function () {
        return this.urlRoot + '/' + this.endPoint + '/';
    }
});

var BaseCollection = Backbone.Collection.extend({
    parse: function (data) {
        return data.data;
    },

    url: function () {
        return BaseModel.prototype.urlRoot + '/' + this.endPoint + '/';
    }
});

module.exports = {
    Model: BaseModel,

    Collection: BaseCollection
};