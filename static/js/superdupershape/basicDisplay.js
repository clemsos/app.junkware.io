var shapeData;
requirejs(['mesh'], function(Mesh) {
    if (!Detector.webgl) {
        Detector.addGetWebGLMessage();
        return;
    }

    var container, camera, scene, renderer, container;

    var width = 600,
        height = 400;

    // get div info
    container = document.getElementById('mesh');
    container.height = width;
    container.width = height;

    // scene
    scene = new THREE.Scene();

    // camera
    camera = new THREE.PerspectiveCamera(35, width / height, .1, 1000)
    camera.updateProjectionMatrix();
    camera.position.z = 300;

    // MESH
    shapeData = {
        t1: 0,
        d1: 0,

        m1: junk.shape.m1,
        n11: junk.shape.n11,
        n12: junk.shape.n12,
        n13: junk.shape.n13,

        t2: 0,
        d2: 0,
        m2: junk.shape.m2,
        n21: junk.shape.n21,
        n22: junk.shape.n22,
        n23: junk.shape.n23,

        c1: 2,
        c2: 4,
        c3: 1
    };

    // console.log(shapeData);

    var mesh = new Mesh(shapeData).scene;
    scene.add(mesh);
    // mesh.scale.set(3, 3, 3);
    // mesh.position.y = 150;
    mesh.position.x = 0;
    camera.lookAt(mesh.position);

    // renderer
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(width, height);
    renderer.shadowMapEnabled = true;
    renderer.shadowMapSoft = true;
    renderer.shadowMapAutoUpdate = true;
    renderer.setFaceCulling('front_and_back', 'cw');

    // LIGHTS
    var spotLight = new THREE.SpotLight(0xffffff);
    spotLight.shadowCameraVisible = false;

    spotLight.position.set(100, 500, 100);
    spotLight.target.position.set(0, 0, 0);

    spotLight.shadowMapWidth = 1000;
    spotLight.shadowMapHeight = 1000;

    spotLight.shadowCameraNear = 450;;
    spotLight.shadowCameraFar = camera.far;
    spotLight.shadowBias = 0.3;

    spotLight.shadowDarkness = 0.8;
    spotLight.castShadow = true;

    // spotLight.shadowCameraVisible = true;

    // append to scene
    scene.add(spotLight);
    scene.add(camera);
    container.appendChild(renderer.domElement);

    // mouse events
    var controls = new THREE.OrbitControls(camera, renderer.domElement);

    // event on resize
    THREEx.WindowResize.bind(renderer, camera);

     function animate() {
        controls.update();
        mesh.rotation.x += 0.01;
        mesh.rotation.y += 0.01;
        requestAnimationFrame(animate);
        render();
    }

    function render() {
        renderer.clear();
        renderer.render(scene, camera);
    }
    
    // start process
    animate();
    // render();

});
