let currentModel = null;

export function loadGLBFile(url, scene, camera, renderer, mixerRef) {
    const loader = new THREE.GLTFLoader();

    // Remove the current model if it exists
    if (currentModel) {
        scene.remove(currentModel);
        currentModel.traverse(child => {
            if (child.isMesh) {
                child.geometry.dispose();
                child.material.dispose();
            }
        });
        if (mixerRef.mixer) {
            mixerRef.mixer.stopAllAction();
        }
        currentModel = null; // Reset currentModel
    }

    loader.load(url, function (gltf) {
        currentModel = gltf.scene;
        currentModel.position.set(0, -2.5, 0);
        currentModel.scale.set(3, 3, 3);

        currentModel.traverse(function (child) {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
                if (child.material.color) {
                    child.material.color.convertSRGBToLinear();
                }
                if (child.material.map) {
                    child.material.map.encoding = THREE.sRGBEncoding;
                }
            }
        });

        scene.add(gltf.scene);

        mixerRef.mixer = new THREE.AnimationMixer(currentModel);
        gltf.animations.forEach(clip => {
            mixerRef.mixer.clipAction(clip).play();
        });

        renderer.render(scene, camera);
    }, undefined, function (error) {
        console.error(error);
    });
}

export function fetchImageList(imageListElement, loadGLBFile, scene, camera, renderer, mixerRef) {
    fetch('/files')
        .then(response => response.json())
        .then(data => {
            const { imageFiles } = data;

            imageFiles.forEach(file => {
                const div = document.createElement('div');
                div.className = 'image-item';
                const img = document.createElement('img');
                img.src = `/input/${file}`;
                div.appendChild(img);

                // Construct the GLB file path with '-merge' suffix
                const folderName = file.replace(/\.[^/.]+$/, "");
                const glbFile = `${folderName}/${folderName}-merge.glb`;

                div.onclick = () => loadGLBFile(`/output/${glbFile}`, scene, camera, renderer, mixerRef);
                imageListElement.appendChild(div);
            });
        })
        .catch(error => console.error('Error fetching file list:', error));
}
