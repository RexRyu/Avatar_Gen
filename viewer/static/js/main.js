import { loadGLBFile, fetchImageList } from './utils.js';
import { openCameraWindow } from './camera.js';

// Initialize Renderer
const container = document.getElementById('container');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);

const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

// Initialize Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xbfe3dd);
scene.fog = new THREE.Fog(0xbfe3dd, 10, 50);

// Initialize Camera
const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 1, 100);
camera.position.set(5, 2, 8);

// Initialize Controls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.5, 0);
controls.update();
controls.enablePan = false;
controls.enableDamping = true;

// Lighting Setup
const ambientLight = new THREE.AmbientLight(0x404040, 2.0);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1.1);
directionalLight.position.set(5, 10, 7.5);
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
directionalLight.shadow.camera.near = 0.5;
directionalLight.shadow.camera.far = 50;
scene.add(directionalLight);

// Ground Setup
const groundTexture = new THREE.TextureLoader().load('https://threejs.org/examples/textures/terrain/grasslight-big.jpg');
const groundGeometry = new THREE.PlaneGeometry(100, 100);
const groundMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff, map: groundTexture });
const ground = new THREE.Mesh(groundGeometry, groundMaterial);

ground.rotation.x = -Math.PI / 2;
ground.position.y = -2.5;
ground.material.map.repeat.set(40, 40);
ground.material.map.wrapS = ground.material.map.wrapT = THREE.RepeatWrapping;
ground.receiveShadow = true;
scene.add(ground);

// Environment Map
new THREE.RGBELoader()
    .setDataType(THREE.UnsignedByteType)
    .setPath('https://threejs.org/examples/textures/equirectangular/')
    .load('royal_esplanade_1k.hdr', function(texture) {
        const envMap = pmremGenerator.fromEquirectangular(texture).texture;
        scene.environment = envMap;
        texture.dispose();
        pmremGenerator.dispose();
    });

// Animation Loop
const mixerRef = { mixer: null };
let currentModel = null;

const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    if (mixerRef.mixer) {
        mixerRef.mixer.update(clock.getDelta());
    }
    renderer.render(scene, camera);
}
animate();

// Handle Window Resize
window.addEventListener('resize', function() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Fetch and Display Image List
const imageList = document.getElementById('image-list');
fetchImageList(imageList, loadGLBFile, scene, camera, renderer, mixerRef);

// Camera Button Functionality
const cameraButton = document.getElementById('cameraButton');
cameraButton.addEventListener('click', openCameraWindow);
