var Marionette = require('backbone.marionette');
var LogView = require('./log');

var ThreeDSliderView = Marionette.ItemView.extend({
  template: require('../../tmpl/3dSlider.hbs'),

  modelEvents: {
    'change:value' : 'updateValues'
  },

  onRender: function() {
    this.logView = new LogView();
    this.logView.render();
    this.$el.find('#log').html(this.logView.$el);
  },

  updateValues: function() {
    var value = this.model.get('value');
    this.$el.find('#x').val(value.x);
    this.$el.find('#y').val(value.y);
    this.$el.find('#z').val(value.z);
  }
});

module.exports = ThreeDSliderView;
