var Marionette = require('backbone.marionette');
var _ = require('underscore');

var chooseRandom = function (list) {
    return list[Math.floor(Math.random() * list.length)];
};

var NavView = Marionette.ItemView.extend({
    template: require('../../tmpl/nav.hbs'),

    templateHelpers: function () {
        return {
            logoFileName: chooseRandom([
                'airware_logo.png',
                'airware_logo.png',
                'airware_logo.png',
                'airware_logo.png',
                'airware_logo.png',
                'airware_logo.png',
                'airware_logo.png',
                'airware_logo.png',
                'airware_logo.png',
                'airwave.png',
            ]),
            productName: 'Motor Burn-in'
        };
    },

    onRender: function () {
        var activeClass = 'btn-primary';
        var inactiveClass = 'btn-default';
        var navButtons = '.motor-nav a';

        this.$el.find(navButtons).removeClass(activeClass);
        var activeButton;
        if (!window.location.hash.length) {
            activeButton = navButtons + ':first-child';
        } else {
            activeButton = navButtons + '[href="' + window.location.hash + '"]';
        }
        this.$el.find(activeButton).addClass(activeClass);
        this.$el.find(navButtons).not(activeButton).addClass(inactiveClass);
    },

    initialize: function () {
        setInterval(function () {
            this.render();
        }.bind(this), 60 * 1000);
    }
});

module.exports = NavView;
