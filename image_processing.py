from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
from PIL import Image
import io
from models import predict_image

image = Blueprint('image', __name__)

@image.route('/')
@login_required
def index():
    return render_template('index.html')

# Load class names
def load_class_names():
    class_names = []
    with open('classes.txt', 'r') as file:
        for line in file:
            class_name = line.strip().split('.')[1].replace('_', ' ')
            class_names.append(class_name)
    return class_names

class_names = load_class_names()

@image.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return redirect(url_for('image.index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('image.index'))
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Open the image file as bytes
    with open(file_path, 'rb') as f:
        image_bytes = f.read()
    
    # Predict the class of the image
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert('RGB')  # Convert image to RGB
    class_id = predict_image(image)
    class_name = class_names[class_id]
    
    # Pass the relative path for the image URL
    image_url = url_for('image.send_file', filename=filename)
    
    return render_template('result.html', class_name=class_name, image_url=image_url)

@image.route('/uploads/<filename>')
@login_required
def send_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
