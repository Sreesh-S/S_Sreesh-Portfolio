/* -------------------------------------------------------------
   THREE.JS 3D BACKGROUND (BLOB & PARTICLES)
   ------------------------------------------------------------- */

(function() {
    const canvas = document.getElementById('three-canvas');
    if (!canvas) return;

    let scene, camera, renderer, blob, particles;
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    init();
    animate();

    function init() {
        // 1. Create Scene
        scene = new THREE.Scene();

        // 2. Camera Setup
        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 100);
        camera.position.z = 5;

        // 3. Renderer Setup
        renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setSize(window.innerWidth, window.innerHeight);

        // 4. Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.15);
        scene.add(ambientLight);

        // Primary Accent Point Light (Cyan)
        const light1 = new THREE.PointLight(0x00F5FF, 2, 50);
        light1.position.set(5, 5, 5);
        scene.add(light1);

        // Secondary Accent Point Light (Purple)
        const light2 = new THREE.PointLight(0x7B61FF, 2, 50);
        light2.position.set(-5, -5, 5);
        scene.add(light2);

        // 5. Creating the Deformed Blob
        // We use a sphere with medium resolution to deform in JS loop
        const geometry = new THREE.SphereGeometry(1.4, 40, 40);
        
        // Cache the original positions of vertices to compute offsets from
        const originalPositions = geometry.attributes.position.clone();
        geometry.userData = { originalPositions: originalPositions };

        // Premium reflective Physical Material
        const material = new THREE.MeshPhysicalMaterial({
            color: 0x121735,
            emissive: 0x05071a,
            roughness: 0.1,
            metalness: 0.9,
            clearcoat: 1.0,
            clearcoatRoughness: 0.1,
            wireframe: false,
            flatShading: false
        });

        blob = new THREE.Mesh(geometry, material);
        scene.add(blob);

        // 6. Creating Space Particles
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 200;
        const posArray = new Float32Array(particlesCount * 3);

        for (let i = 0; i < particlesCount * 3; i += 3) {
            // Distribute particles in a box around the blob
            posArray[i] = (Math.random() - 0.5) * 10;
            posArray[i+1] = (Math.random() - 0.5) * 10;
            posArray[i+2] = (Math.random() - 0.5) * 10;
        }

        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

        const particlesMaterial = new THREE.PointsMaterial({
            size: 0.02,
            color: 0x00F5FF,
            transparent: true,
            opacity: 0.6
        });

        particles = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particles);

        // 7. Event Listeners
        window.addEventListener('resize', onWindowResize);
        document.addEventListener('mousemove', onDocumentMouseMove);
    }

    function onDocumentMouseMove(event) {
        // Normalize mouse coordinates (-1 to 1)
        mouseX = (event.clientX - windowHalfX) / 100;
        mouseY = (event.clientY - windowHalfY) / 100;
    }

    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    function animate() {
        requestAnimationFrame(animate);

        const time = Date.now() * 0.001;

        // 1. Deform Blob Geometry in Real Time
        if (blob) {
            const positionAttribute = blob.geometry.attributes.position;
            const originalPositions = blob.geometry.userData.originalPositions;
            
            for (let i = 0; i < positionAttribute.count; i++) {
                const x = originalPositions.getX(i);
                const y = originalPositions.getY(i);
                const z = originalPositions.getZ(i);

                // Use wave mathematics (sine/cosine) with noise combinations to create fluid deformation
                const waveOffset = Math.sin(x * 1.5 + time * 1.2) * 0.12 + 
                                   Math.cos(y * 1.5 + time * 1.5) * 0.12 +
                                   Math.sin(z * 1.5 + time * 1.0) * 0.12;

                positionAttribute.setXYZ(
                    i,
                    x + x * waveOffset,
                    y + y * waveOffset,
                    z + z * waveOffset
                );
            }
            positionAttribute.needsUpdate = true;

            // Slow idle rotations
            blob.rotation.x = time * 0.15;
            blob.rotation.y = time * 0.10;
        }

        // 2. Rotate background particles
        if (particles) {
            particles.rotation.y = time * 0.03;
            particles.rotation.x = time * 0.015;
        }

        // 3. Smooth mouse parallax interpolation (easing)
        targetX += (mouseX - targetX) * 0.05;
        targetY += (mouseY - targetY) * 0.05;

        camera.position.x = targetX * 0.3;
        camera.position.y = -targetY * 0.3;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }
})();
