/**
 * Created by ld on 8/5/15.
 */

var RowView = require('./common/RowView');
var ThermostatModel = require('./ThermostatModel');
var ThermostatChart = require('./ThermostatChart');
var KegsCollection = require('./KegsCollection');
var KegsTable = require('./KegsView');
var BeersCollection = require('./BeersCollection');
var BeersTable = require('./BeersTable');
var EventsCollection = require('./EventsCollection');
var EventLog = require('./EventLog');

module.exports = {

    thermostat: function(viewPort) {
        var thermostat = new ThermostatModel();

        thermostat
            .fetch()
            .then(function() {

                var ThermostatPage = RowView.extend({
                    childViews: [
                        ThermostatChart.extend({
                            model: thermostat
                        })
                    ]
                });

                viewPort.show(new ThermostatChart({
                    model: thermostat
                }));
            });
    },

    kegs: function(viewPort) {
        var kegs = new KegsCollection();
        var beers = new BeersCollection();

        kegs
            .fetch()
            .then(function() {
                beers
                    .fetch()
                    .then(function() {

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

        events
            .fetch()
            .then(function() {
                var EventsPage = RowView.extend({
                    childViews: [
                        EventLog.extend({
                            collection: events
                        })
                    ]
                });

                viewPort.show(new EventsPage());
            });
    }
};
