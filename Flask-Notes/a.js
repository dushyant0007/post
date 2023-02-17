// Set up the scene, camera, and renderer
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Add objects to the scene
var sun = new THREE.Mesh(
  new THREE.SphereGeometry(5, 32, 32),
  new THREE.MeshBasicMaterial({ color: 0xffff00 })
);
scene.add(sun);

var earth = new THREE.Mesh(
  new THREE.SphereGeometry(1, 32, 32),
  new THREE.MeshBasicMaterial({ color: 0x0000ff })
);
earth.position.x = 10;
scene.add(earth);

// Animate the scene
function animate() {
  requestAnimationFrame(animate);
  earth.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
