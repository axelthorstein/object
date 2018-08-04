#pylint: disable=global-at-module-level

import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

global admin
admin = firebase_admin.initialize_app(
    credentials.Certificate(
        '/Users/axelthor/credentials/firebase_credentials.json'),
    name='object-is',
    options={"databaseURL": "https://object-is.firebaseio.com/"})


class Firebase:

    def __init__(self, file_path):
        self.file_path = file_path

    def download_image(self):
        bucket = storage.bucket(name="object-is.appspot.com", app=admin)
        bucket.blob(self.file_path).download_to_filename(self.file_path)

    def clean_up(self):
        os.remove(self.file_path)
