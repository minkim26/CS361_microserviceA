from flask import Flask, jsonify, send_from_directory, request
import os
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CONFIG_PATH = 'config.txt'

def get_image_directory():
    with open(CONFIG_PATH, 'r') as file:
        config_lines = file.readlines()
    config = dict(line.strip().split('=') for line in config_lines)
    return config.get('image_directory', 'images')

@app.route('/random-profile-image', methods=['GET'])
def random_profile_image():
    image_directory = get_image_directory()
    images = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]
    if not images:
        return jsonify({"error": "No images found"}), 404
    image_filename = random.choice(images)
    image_url = request.host_url + 'images/' + image_filename
    return jsonify({"image_url": image_url})

@app.route('/images/<filename>')
def get_image(filename):
    image_directory = get_image_directory()
    return send_from_directory(image_directory, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
