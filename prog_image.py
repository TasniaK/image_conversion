from flask import Flask, request

# make flask app
app = Flask(__name__)

# make api accept image uploads at image/upload/ and return unique identifier.
@app.route('/image/upload/')
def upload_image():
    return 'Upload an image here.'

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
