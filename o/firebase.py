import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


global admin
admin = firebase_admin.initialize_app(credentials.Certificate('config/firebase_credentials.json'),
                                      name='redheads-181023',
                                      options={"databaseURL": "https://redheads-181023.firebaseio.com/"})


class Firebase:

    def __init__(self, file_path):
        self.file_path = file_path

    def download_image(self):
        bucket = storage.bucket(name="redheads-181023.appspot.com", app=admin)
        bucket.blob(self.file_path).download_to_filename(self.file_path)

    def clean_up(self):
        os.remove(self.file_path)
