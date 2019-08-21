import os
from flask import Flask, request, flash, redirect, send_file
import uuid
from PIL import Image
import glob
import config
from werkzeug.exceptions import BadRequest

# make flask app
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.secret_key = config.SECRET_KEY


@app.route('/image/<string:image_identifier>/', methods=['GET'])
def get_image(image_identifier):
    """Return image to user, convert if format parameter is passed to url."""
    # grab file path.
    file_path = ''
    current_extension = ''
    for file in glob.glob('{0}/{1}.*'.format(app.config['UPLOAD_FOLDER'], image_identifier)):
        file_path = file.split('.')[1]
        current_extension = file.split('.')[2]
    image = Image.open(".{0}.{1}".format(file_path, current_extension))

    # if image_format parameter is passed to url.
    image_format = request.args.get('format')
    if image_format:
        # if image format requested is existing format.
        if image_format == current_extension:
            return send_file(".{0}.{1}".format(file_path, current_extension))
        else:
            new_filename = '{0}.{1}'.format(image_identifier, image_format)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],new_filename), image_format)
            current_extension = image.format

    return send_file(".{0}.{1}".format(file_path, current_extension))

def has_allowed_ext(filename):
    """Check if image being uploaded has one of the allowed extensions."""
    extension_given = filename.rsplit('.', 1)[1].lower()
    if extension_given in ALLOWED_EXTENSIONS:
        return extension_given
    raise BadRequest('This image extension is not allowed.')

# upload image and return unique identifier.
@app.route('/image/upload/', methods=['POST'])
def upload_image():
    """Upload image via api, return the unique identifier for that image."""
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

        # otherwise, upload file to upload folder.
        extension = has_allowed_ext(file.filename)
        if file and extension:
            unique_identifier = str(uuid.uuid4())
            unique_filename = "{0}.{1}".format(unique_identifier, extension)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            return 'Your unique identifier is: {}'.format(unique_identifier)

# documentation accessible through api - swagger.

if __name__ == '__main__':
    app.run()
