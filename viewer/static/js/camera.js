export function openCameraWindow() {
    const cameraWindow = window.open('', 'cameraWindow', 'width=800,height=600');
    cameraWindow.document.write(`
        <html>
        <head>
            <title>Camera View</title>
            <style>
                body { margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #000; flex-direction: column; }
                video { max-width: 100%; max-height: 100%; }
                #controls { display: flex; justify-content: center; margin-top: 10px; }
                button { margin: 5px; padding: 10px; font-size: 16px; }
            </style>
        </head>
        <body>
            <video id="video" autoplay></video>
            <canvas id="canvas" style="display:none;"></canvas>
            <div id="controls">
                <button id="captureButton">Capture</button>
                <button id="okButton" style="display:none;">OK</button>
                <button id="againButton" style="display:none;">Retry</button>
            </div>
            <script>
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const captureButton = document.getElementById('captureButton');
                const okButton = document.getElementById('okButton');
                const againButton = document.getElementById('againButton');

                // Access the camera
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(stream => {
                        video.srcObject = stream;
                    })
                    .catch(err => {
                        console.error('Error accessing camera: ', err);
                    });

                captureButton.addEventListener('click', () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    const context = canvas.getContext('2d');
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    captureButton.style.display = 'none';
                    okButton.style.display = 'inline';
                    againButton.style.display = 'inline';
                    video.style.display = 'none';
                    canvas.style.display = 'block';
                });

                againButton.addEventListener('click', () => {
                    captureButton.style.display = 'inline';
                    okButton.style.display = 'none';
                    againButton.style.display = 'none';
                    video.style.display = 'block';
                    canvas.style.display = 'none';
                });

                okButton.addEventListener('click', () => {
                    canvas.toBlob(blob => {
                        const formData = new FormData();
                        formData.append('file', blob, 'capture.jpg');
                        fetch('/upload', {
                            method: 'POST',
                            body: formData
                        }).then(response => {
                            if (response.ok) {
                                alert('Image saved successfully!');
                                window.close(); // Close the camera window
                            } else {
                                alert('Error saving image.');
                            }
                        }).catch(error => {
                            console.error('Error:', error);
                            alert('Error saving image.');
                        });
                    }, 'image/jpeg');
                });
            </script>
        </body>
        </html>
    `);
}
