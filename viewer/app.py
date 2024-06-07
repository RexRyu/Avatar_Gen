from flask import Flask, jsonify, send_from_directory, render_template, request
import os
import time

app = Flask(__name__, static_folder='static', template_folder='templates')

output_dir = "../output"
input_dir = "../input"
animations_dir = "../animations"

@app.route('/files')
def list_files():
    glb_files = []
    image_files = []
    animation_files = []
    
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.glb'):
                glb_files.append(os.path.relpath(os.path.join(root, file), output_dir))
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.relpath(os.path.join(root, file), input_dir))
    
    for root, _, files in os.walk(animations_dir):
        for file in files:
            if file.endswith('.fbx'):
                animation_files.append(os.path.relpath(os.path.join(root, file), animations_dir))
    
    return jsonify({"glbFiles": glb_files, "imageFiles": image_files, "animationFiles": animation_files})

@app.route('/output/<path:filename>')
def serve_output_file(filename):
    return send_from_directory(output_dir, filename)

@app.route('/input/<path:filename>')
def serve_input_file(filename):
    return send_from_directory(input_dir, filename)

@app.route('/animations/<path:filename>')
def serve_animation_file(filename):
    return send_from_directory(animations_dir, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        timestamp = int(time.time())
        filename = f"{timestamp}.jpg"
        file.save(os.path.join(input_dir, filename))
        return 'File saved', 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5005)
