from flask import Flask, jsonify, send_from_directory, render_template
import os

app = Flask(__name__)
output_dir = "../output"

@app.route('/files')
def list_files():
    glb_files = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.glb'):
                glb_files.append(os.path.relpath(os.path.join(root, file), output_dir))
    return jsonify(glb_files)

@app.route('/output/<path:filename>')
def serve_file(filename):
    return send_from_directory(output_dir, filename)

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('.', path)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5008)
