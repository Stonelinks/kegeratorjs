var express = require('express'),
	path	= require('path'),
	_ = require('lodash'),
	url	= require('url'),
	qr	= require('qr-image');
	ip = require('ip');

function WebService() {
	// create the express app
	this.app = express();

	// stash off where our static root is
	this.root = path.resolve(__dirname, '../../../build');

	// setup socket
	this.server = require('http').Server(this.app);
	var mosca = require('mosca');
	mqttServ = new mosca.Server({});
	mqttServ.on('clientConnected', function(client) {
		console.log(client.id + ' connected');
	});
	mqttServ.attachHttpServer(this.server);
}

WebService.prototype.start = function() {
	// serve our static content
	this.app.use(express.static(this.root));

	this.app.get('/qr', function(req, res, next) {
		var u = url.format({
			protocol: 'http',
			hostname: ip.address(),
			port: this.server.address().port,
			pathname: '/controls'
		});
		var code = qr.image(u, { type: 'svg' });
		res.type('svg');
		code.pipe(res);
	}.bind(this));

	// route all request to the index.html so Marionette can handle routing
	this.app.use('*', function(req, res, next) {
		res.sendFile(this.root + '/index.html');
	}.bind(this));

	this.server.listen(4545, function() {
		console.log('Webserver started');
	}.bind(this));
};

module.exports = WebService;
