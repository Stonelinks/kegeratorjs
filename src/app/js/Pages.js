/**
 * Created by ld on 8/5/15.
 */

var RowView = require('./common/RowView');
var ThermostatModel = require('./ThermostatModel');
var ThermostatRealtimeChart = require('./ThermostatRealtimeChart');
var ThermostatEventChart = require('./ThermostatEventChart');
var KegsCollection = require('./KegsCollection');
var KegsTable = require('./KegsView');
var BeersCollection = require('./BeersCollection');
var BeersTable = require('./BeersTable');
var EventsCollection = require('./EventsCollection');
var EventLog = require('./EventLog');

module.exports = {

    realtime: function(viewPort) {
        var thermostat = new ThermostatModel();

        thermostat.fetch().then(function() {

            var ThermostatPage = RowView.extend({
                childViews: [
                    ThermostatRealtimeChart.extend({
                        model: thermostat
                    })
                ]
            });

            viewPort.show(new ThermostatRealtimeChart({
                model: thermostat
            }));
        });
    },

    kegs: function(viewPort) {
        var kegs = new KegsCollection();
        var beers = new BeersCollection();

        kegs.fetch().then(function() {
            beers.fetch().then(function() {

                kegs.forEach(function(keg) {
                    keg.set('beer', beers.findWhere({
                        id: keg.get('beerId')
                    }));
                });

                var BeerPage = RowView.extend({
                    childViews: [
                        KegsTable.extend({
                            collection: kegs
                        }),
                        BeersTable.extend({
                            collection: beers
                        })
                    ]
                });

                viewPort.show(new BeerPage());
            });
        });
    },

    history: function(viewPort) {
        var events = new EventsCollection();
        var thermostat = new ThermostatModel();

        thermostat.fetch().then(function() {
            events.fetch().then(function() {
                var EventsPage = RowView.extend({
                    childViews: [
                        ThermostatEventChart.extend({
                            model: thermostat,
                            collection: events
                        })
                    ]
                });

                viewPort.show(new EventsPage());
            });
        });
    }
};
