import os
from flask import Flask, request, flash, redirect, send_file
import uuid
from PIL import Image
import glob

# make flask app
UPLOAD_FOLDER = './uploaded_images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def has_allowed_ext(filename):
    extension_given = filename.rsplit('.', 1)[1].lower()
    if extension_given in ALLOWED_EXTENSIONS:
        return extension_given
    return None

# upload image and return unique identifier.
@app.route('/image/upload/', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        # if no file in request.
        if 'file' not in request.files:
            print('No file given in request')
            return redirect(request.url)

        file = request.files['file']

        # if no file selected.
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)

# download image when image/{unique identifier} is accessed
@app.route('/image/<string:image_identifier>/', methods=['GET'])
def get_image(image_identifier):
    return 'showing image: {}'.format(image_identifier)

# download image in specified format when image/{unique identifier}/{image format} is accessed.
@app.route('/image/<string:image_identifier>/<string:image_format>/', methods=['GET'])
def get_converted_image(image_identifier, image_format):
    return 'showing image: {} in the format: {}'.format(image_identifier, image_format)

# write tests that test the image upload, download and file format conversion

# documentation, comments, readme.md. documentation accessible through api - swagger.

if __name__ == '__main__':
    app.run()
