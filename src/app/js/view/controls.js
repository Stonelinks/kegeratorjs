var Marionette = require('backbone.marionette');
	Backbone = require('backbone'),
	screenfull	= require('screenfull'),
	JoystickView	= require('./joystick');
	AttitudeView	= require('./attitude');

var ControlsView = Marionette.ItemView.extend({
	template: require('../../tmpl/controls.hbs'),

	onRender: function() {
		var joystickModelLeft = new Backbone.Model({x: 0, y: 0});
		var joystickModelRight = new Backbone.Model({x: 0, y: 0});

		var joystickLeft = new JoystickView({
			el: this.$el.find('#joystick-left'),
			model: joystickModelLeft
		}).render();
		var joystickRight = new JoystickView({
			el: this.$el.find('#joystick-right'),
			model: joystickModelRight
		}).render();

		var attitudeModel = new Backbone.Model();
		var attitude = new AttitudeView({
			el: this.$el.find('#attitude'),
			model: attitudeModel
		});
		attitude.render();

		var client = require('mqtt').connect();
		client.subscribe('vehicle/attitude');
		client.on('message', function(topic, payload) {
			attitudeModel.set(JSON.parse(payload));
		});
		var sendControls = function() {
			client.publish('vehicle/controls', JSON.stringify({
				yaw: joystickModelLeft.get('x'),
				throttle: joystickModelLeft.get('y'),
				pitch: joystickModelRight.get('y'),
				roll: joystickModelRight.get('x')
			}), {qos: 2});
		};


		joystickModelLeft.on('change', sendControls);
		joystickModelRight.on('change', sendControls);

		this.$el.find('#fullscreen').click(function() {
			if (screenfull.enabled) {
			    screenfull.request(this.el);
			}
		});

		window.addEventListener('load', function() {
			// Set a timeout...
			setTimeout(function() {
				// Hide the address bar!
				window.scrollTo(0, 100);
			}, 100);
		});

	}

});

module.exports = ControlsView;
