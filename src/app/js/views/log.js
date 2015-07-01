var Marionette = require('backbone.marionette');
  Backbone = require('backbone');

var LogLineView = Marionette.ItemView.extend({
  tagName: 'tr',
  template: require('../../tmpl/logline.hbs')
});

var LogView = Marionette.CollectionView.extend({
  tagName: 'table',
  className: 'log table table-striped',
  template: false,
  childView: LogLineView,
  tail: true,

  initialize: function() {
    this.collection = new Backbone.Collection();
    console.log('started logs!!!!!');
    // var client = require('mqtt').connect();
    // client.subscribe('vehicle/log/trace');
    // client.on('message', function(topic, payload) {
          // console.log(payload.toString())
      // this.collection.add(new Backbone.Model({msg: payload}));
    // }.bind(this));
  },

  onAddChild: function() {
    if (this.collection.length > 1000) {
      this.collection.shift();
    }
    if (this.tail && this.el.parentElement) {
      var elem = this.el.parentElement;
      elem.scrollTop = elem.scrollHeight;
    }
  }
});



module.exports = LogView;
