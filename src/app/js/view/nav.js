var Marionette = require('backbone.marionette');
var _ = require('underscore');

var chooseRandom = function(list) {
  return list[Math.floor(Math.random() * list.length)];
};

var NavView = Marionette.ItemView.extend({
  template: require('../../tmpl/nav.hbs'),
  
  serializeData: function() {
    return {
      logoFileName: chooseRandom([
        'airwave.png',
        'unmanned_innovations.png',
        '3DR_logo_short_color.gif'
      ]),
      productName: chooseRandom([
        'Kegerator',
        'Kegerator',
        'Kegerator',
        'JIRA for beer???',
        '7geese',
        'Pizza Delivery Network',
        'Payroll System'
      ])
    }
  },
  
  selectActiveButton: function() {
    this.$el.find('.kegerator-nav a').removeClass('active');
    var activeButton;
    if (!window.location.hash.length) {
      activeButton = '.kegerator-nav a:first-child'
    } else {
      activeButton = '.kegerator-nav a[href="' + window.location.hash + '"]'
    }
    this.$el.find(activeButton).addClass('active');
  }
});

module.exports = NavView;
