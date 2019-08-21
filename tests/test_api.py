import io
from mock import patch, Mock
from prog_image import image_save
import os

# Use client created in conftest to carry out requests.

CORRECT_FILE = './tests/test_bunny.jpg'
INCORRECT_FILE = './tests/test_bunny_wrong_extension.j'

def upload_test_image(image_filename, client):
    """Upload a given image file through api with test client."""
    with open(image_filename, 'rb') as image_file:
        image = io.BytesIO(image_file.read())
    data = {'file': (image, image_filename)}
    response = client.post("/image/upload/", data=data, follow_redirects=True,
                           content_type='multipart/form-data')
    return response

def test_upload_image(client):
    """Test if an image can be uploaded via the api."""
    response = upload_test_image(CORRECT_FILE, client)
    assert response.status_code == 200

def test_has_allowed_ext(client):
    """Test if incorrect image extensions raise an error."""
    response = upload_test_image(INCORRECT_FILE, client)
    print(response.data)
    assert response.status_code == 400

def test_get_image_original(client):
    """Test if an image can be returned."""
    upload_response = upload_test_image(CORRECT_FILE, client)
    identifier = ((upload_response.data).decode("utf-8")).split(': ')[1]

    response = client.get('image/{}/'.format(identifier))

    assert response.status_code == 200

def test_get_image_converted(client):
    """Test if a converted image can be returned using a given format."""
    upload_response = upload_test_image(CORRECT_FILE, client)
    extension = 'png'
    identifier = ((upload_response.data).decode("utf-8")).split(': ')[1]

    response = client.get('image/{0}/?format={1}'.format(identifier, extension))

    assert response.status_code == 200

def test_get_image_converted(client):
    """Test if a converted image hits the image_save() function."""
    upload_response = upload_test_image(CORRECT_FILE, client)
    identifier = ((upload_response.data).decode("utf-8")).split(': ')[1]
    extension = 'png'

    # if converted file already exists, remove
    if os.path.exists('./uploaded_images/{0}.{1}'.format(identifier, extension)):
        os.remove('./uploaded_images/{0}.{1}'.format(identifier, extension))

    with patch('prog_image.image_save', side_effect=image_save) as mock:
        client.get('image/{0}/?format={1}'.format(identifier, extension))
        assert mock.call_args_list[0].args[1] == '{0}.{1}'.format(identifier, extension)
        assert mock.call_args_list[0].args[2] == extension

def test_get_image_format_same_as_original(client):
    """Test if image format given is same as original format, image is not converted."""
    upload_response = upload_test_image(CORRECT_FILE, client)
    identifier = ((upload_response.data).decode("utf-8")).split(': ')[1]
    extension = 'jpg'

    client.get('image/{0}/?={1}'.format(identifier, extension))
    mock = Mock()
    function = mock.image_save()
    assert not function.called

