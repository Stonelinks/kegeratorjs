var gulp 		= require('gulp'),
	package		= require('./package.json'),
	tap 		= require('gulp-tap'),
	webserver = require('gulp-webserver'),
	rename		= require('gulp-rename'),
	clean		= require('gulp-clean'),
	browserify	= require('browserify'),
	handlebars 	= require('handlebars'),
	uglify = require('gulp-uglify'),
	sourcemaps = require('gulp-sourcemaps'),
	less = require('gulp-less'),
	buffer = require('vinyl-buffer'),
	transform 	= require('vinyl-transform'),
	source = require('vinyl-source-stream'),
	nodemon	= require('gulp-nodemon')

var path = {
	tmpl: './src/app/tmpl/**/*.hbs',
	style: './src/app/style/**/*.less',
	js: './src/app/js/**/*.js',
	images: './src/app/images/**/*.*',
	server: './src/server/**.js',
	index: './src/app/index.hbs'
}

gulp.task('js', function() {
	var bundler = browserify({
		entries: ['./src/app/js/app.js'],
		debug: true
	});

	var bundle = function() {
		return bundler
			.bundle()
			.pipe(source(package.name + "." + package.version + '.min.js'))
			.pipe(buffer())
			.pipe(sourcemaps.init({loadMaps: true}))
			//.pipe(uglify())
			.pipe(sourcemaps.write('./'))
			.pipe(gulp.dest('./build/js/'));
	};
	return bundle();
});

gulp.task('images', function() {
	gulp.src(path.images)
		.pipe(gulp.dest('./build/images'));
});

gulp.task('style', function() {
	gulp.src(path.style)
		.pipe(less({
	      paths: [ './node_modules/bootstrap/less' ]
	    }))
    .pipe(gulp.dest('./build/style'));

});

gulp.task('index', function() {
  gulp.src(path.index)
    .pipe(tap(function(file, t) {
		var template = handlebars.compile(file.contents.toString())
		var html = template(package)
		file.contents = new Buffer(html, "utf-8")
    }))
    .pipe(rename(function(path) {
		path.extname = ".html"
    }))
    .pipe(gulp.dest("build/"))
});

gulp.task('webserver', function() {
  nodemon({ 
  	script: 'src/server/index.js', 
  	ext: 'js'
  });
});

gulp.task('clean', function() {
	return gulp.src('./build')
		.pipe(clean());
});

gulp.task('build', ['js', 'style', 'index', 'images']);

gulp.task('watch', ['build'], function() {
	gulp.watch(path.js, ['js']);
	gulp.watch(path.style, ['style']);
	gulp.watch(path.tmpl, ['js']);
	gulp.watch(path.index, ['index']);
});

gulp.task('develop', ['watch', 'webserver']);

gulp.task('default', ['build']);
