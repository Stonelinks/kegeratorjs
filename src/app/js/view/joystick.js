var Marionette = require('backbone.marionette');
	Backbone = require('backbone'),
	paper	= require('paper/dist/paper-full');

var JoystickView = Marionette.ItemView.extend({
	template: false,
	tagName: 'canvas',
	radius: 20,

	modelEvents: {
		'change' : 'draw'
	},

	events: {
		'mousedown' : 'startControl',
		'mouseup' : 'stopControl',
		'mousemove' : 'onControl',
		'mousemove' : 'stopControl',
		'touchstart' : 'startControl',
		'touchend' : 'stopControl',
		'touchleave' : 'stopControl',
		'touchmove' : 'onControl'
	},


	onRender: function() {
		this.measure();
		this.paper = new paper.PaperScope();
		this.paper.setup(this.el);

		this.target = new this.paper.Path.Circle(new this.paper.Point(this.center.x, this.center.y), 50);
		this.target.fillColor = new paper.Color(1, 1, 1, .2);
		this.target.strokeColor = new paper.Color(1, 1, 1, .8);
		this.target.strokeWidth = 3;
		//this.target.on('mousedown', this.startControl.bind(this));

		this.thumb = new this.paper.Path.Circle(new this.paper.Point(this.center.x, this.center.y), 15);
		this.thumb.fillColor = 'white';
		this.thumb.visible = false;
/*
		this.tool = new this.paper.Tool();
		this.tool.onMouseMove = this.onControl.bind(this);
		this.tool.onMouseUp = this.stopControl.bind(this);
*/
		this.paper.view.draw();
	},

	draw: function() {
		console.log('drawin!');
		this.thumb.setPosition(new this.paper.Point((this.model.get('x') + 1) * this.center.x,
											 	(this.model.get('y') + 1) * this.center.y));
	},

	measure: function() {
		this.dimensions = {
			width: this.el.width,
			height: this.el.height
		};
		this.center = {
			x: this.dimensions.width / 2,
			y: this.dimensions.height / 2
		};
	},

	startControl: function(e) {
		//e.preventDefault();
		this.controlling = true;
		/*this.model.set({
			x: (e.point.x/this.dimensions.width - 0.5) * 2,
			y: (e.point.y/this.dimensions.height - 0.5) * 2
		});*/
		this.thumb.visible = true;
	},

	getCoords: function(e) {
		if (e.originalEvent instanceof TouchEvent) {
			var local = {
				x: this.$el.offset().left,
				y: this.$el.offset().top
			};
			return {
				x: e.originalEvent.targetTouches[0].pageX - local.x,
				y: e.originalEvent.targetTouches[0].pageY - local.y
			};
		} else if (e.originalEvent instanceof MouseEvent) {
			return {
				x: e.offsetX,
				y: e.offsetY
			};
		}
		/*return {
			x: (e.point.x/this.dimensions.width - 0.5) * 2,
			y: (e.point.y/this.dimensions.height - 0.5) * 2
		}*/
	},

	stopControl: function(e) {
		this.controlling = false;
		this.thumb.visible = false;
		this.model.set({
			x: 0,
			y: 0
		});
	},

	onControl: function(e) {
		if (this.controlling) {
			var coords = this.getCoords(e);
			this.model.set({
				x: (coords.x / this.dimensions.width - 0.5) * 2,
				y: (coords.y / this.dimensions.height - 0.5) * 2
			});
			//console.log(e);
			//this.model.set(this.getCoords(e));
		}
	}
});


module.exports = JoystickView;
