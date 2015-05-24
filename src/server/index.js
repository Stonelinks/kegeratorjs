var cluster	= require('cluster');

if (cluster.isMaster) {
	cluster.fork({service: 'web'});
	cluster.fork({service: 'kegerator'});
} else {
	console.log('starting service: %s', process.env.service);
	var Service = require('./services/' + process.env.service);
	var service = new Service();
	service.start();
}
