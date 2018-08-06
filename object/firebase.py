#pylint: disable=global-at-module-level

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from configs.config import CREDENTIALS_FILE

global admin

admin = firebase_admin.initialize_app(
    credentials.Certificate(CREDENTIALS_FILE),
    name='object-is',
    options={'databaseURL': 'https://object-is.firebaseio.com/'})


class Firebase:
    """
    An interface for Firebase Google Cloud Storage.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def download_image(self):
        """Download the given image from Firebase to a local directory.
        """
        base_image_directory = 'images/'

        if not os.path.exists(base_image_directory):
            os.makedirs(base_image_directory)

        bucket = storage.bucket(name='object-is.appspot.com', app=admin)
        bucket.blob(self.file_path).download_to_filename(self.file_path)

    def clean_up(self):
        """Remove the file that was downloaded locally.
        """
        os.remove(self.file_path)
