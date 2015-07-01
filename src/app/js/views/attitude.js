var Marionette = require('backbone.marionette'),
  $ = require('jquery'),
  THREE = require('three');

var AttitudeView = Marionette.ItemView.extend({
  template: false,
  tagName: 'canvas',

  modelEvents: {
    'change' : 'setAttitude'
  },

  onRender: function() {
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.el,
      alpha: true
    });
    this.renderer.setSize(this.el.width, this.el.height);
    this.camera = new THREE.PerspectiveCamera(75, this.el.width / this.el.height, 0.1, 1000);
    this.scene = new THREE.Scene();

    var geometry = new THREE.SphereGeometry(5, 32, 32);
    var material = new THREE.MeshBasicMaterial();
    material.map = THREE.ImageUtils.loadTexture('images/texture.jpg');
    this.sphere = new THREE.Mesh(geometry, material);


    /*var indicatorGeometry = new THREE.PlaneGeometry( 5, 5 );
    var indiatorMaterial = new THREE.MeshBasicMaterial({alpha: true});
    material.map = THREE.ImageUtils.loadTexture('images/indicator.png')
    var plane = new THREE.Mesh( indicatorGeometry, indiatorMaterial );
    plane.position.z = 6*/
    //this.scene.add( plane );

    this.scene.add(this.sphere);
    this.camera.position.z = 10;
    this.renderCanvas();
  },

  renderCanvas: function() {
    requestAnimationFrame(this.renderCanvas.bind(this));
    this.renderer.render(this.scene, this.camera);
  },

  setAttitude: function() {
    //console.log(this.model.toJSON());
    this.sphere.rotation.x = this.model.get('pitch');
    //this.sphere.rotation.y = this.model.get('yaw');
    this.sphere.rotation.z = this.model.get('roll');
  }
});

module.exports = AttitudeView;
