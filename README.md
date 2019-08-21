# image_conversion
A microservice allowing users to upload images and download them in a different format.

# Setup
pip install -r requirements.txt

Note: to add an image, you'll need to use Postman or a similar application.
* Set the method to 'POST', endpoint to 'http://127.0.0.1:5000/image/upload/'.
* Under 'Body', select 'form-data', select the key type to 'file' and put the key value as 'file'.
* Select an image of choice and hit send to receive the images unique identifier.

# Thoughts

## Packages Used

* I know that Pillow is built on top of PIL as an extension to allow for python3 use. But it
seemed PIL fit my basic image manipulation needs.

* I used uuid to create the unique identifiers as the api would be used in-house and does not need
an extensively complex identifier.

* I used pytest for my tests as I've used it many times before and I am able to create fixtures.

* I used the mock library to mock the image_save() function. This was so I could check whether it
was being called or not. Vital to determine if conversion of image format had taken place.

## Thoughts on the Challenge

* I created the config file to keep any setup constants in one place. This should make it easier
to set up.

* I didn't use docker as I am limited on my old Mac. In any case, all my file paths are relative.

* While writing the tests I realised I needed to make sure the originally uploaded image was
distinguishable from the converted ones. I first added an underscore to the end of the extension,
but this creates issues with returning the image later on. So I then added the underscore to the
end of the filename (which is the identifier).