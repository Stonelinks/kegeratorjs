var Marionette = require('backbone.marionette');
var _ = require('underscore');

var chooseRandom = function(list) {
  return list[Math.floor(Math.random() * list.length)];
};

var NavView = Marionette.ItemView.extend({
  template: require('../tmpl/nav.hbs'),

  serializeData: function() {
    return {
      logoFileName: chooseRandom([
        'airware_logo.png',
        'airware_logo.png',
        'airware_logo.png',
        'airware_logo.png',
        'airware_logo.png',
        'airwave.png',
        'unmanned_innovations.png',
        '3DR_logo_short_color.gif'
      ]),
      productName: chooseRandom([
        'Kegerator',
        'Kegerator',
        'Kegerator',
        'JIRA for beer',
        '7geese',
        'Pizza Delivery Network',
        'Payroll System'
      ])
    };
  },

  selectActiveButton: function() {
    var activeClass = 'btn-primary';
    var inactiveClass = 'btn-default';
    var navButtons = '.kegerator-nav a';

    this.$el.find(navButtons).removeClass(activeClass);
    var activeButton;
    if (!window.location.hash.length) {
      activeButton = navButtons + ':first-child';
    } else {
      activeButton = navButtons + '[href="' + window.location.hash + '"]';
    }
    this.$el.find(activeButton).addClass(activeClass);
    this.$el.find(navButtons).not(activeButton).addClass(inactiveClass);
  }
});

module.exports = NavView;
