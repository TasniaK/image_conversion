import io
import random
from config import ALLOWED_EXTENSIONS

# Use client created in conftest to carry out requests.

CORRECT_FILE = './tests/test_bunny.jpg'
INCORRECT_FILE = './tests/test_bunny_wrong_extension.j'

def upload_test_image(image_filename, client):
    with open(image_filename, 'rb') as image_file:
        image = io.BytesIO(image_file.read())
    data = {'file': (image, image_filename)}
    response = client.post("/image/upload/", data=data, follow_redirects=True,
                           content_type='multipart/form-data')
    return response

def test_upload_image(client):
    response = upload_test_image(CORRECT_FILE, client)
    assert response.status_code == 200

def test_has_allowed_ext(client):
    response = upload_test_image(INCORRECT_FILE, client)
    print(response.data)
    assert response.status_code == 400

def test_get_image_original(client):
    upload_response = upload_test_image(CORRECT_FILE, client)
    identifier = ((upload_response.data).decode("utf-8")).split(': ')[1]

    response = client.get('image/{}/'.format(identifier))

    assert response.status_code == 200

def test_get_image_converted(client):
    upload_response = upload_test_image(CORRECT_FILE, client)
    identifier = ((upload_response.data).decode("utf-8")).split(': ')[1]

    extension = random.choice(list(ALLOWED_EXTENSIONS))
    response = client.get('image/{0}/?={1}'.format(identifier, extension))

    assert response.status_code == 200

#get_image(image_identifier) original
#get_image(image_identifier) convert
