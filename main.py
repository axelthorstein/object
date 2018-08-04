import os

from flask import Flask
from flask import render_template
from flask import redirect

from obj.graphql import GraphQL
from obj.detect import Detector
from obj.firebase import Firebase
from configs.config import SEQUENCES

app = Flask(__name__)


@app.route('/capture')
def capture():
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "config/cloud_credentials.json"
    return render_template('capture.html')


@app.route('/products')
def get_graphql_products():
    return str(GraphQL.get_products())


@app.route('/images/<image_id>', methods=["GET"])
def images(image_id):

    file_path = "images/" + image_id + ".png"

    db = Firebase(file_path)
    db.download_image()

    detector = Detector(file_path)

    ring = detector.detect()

    if ring.is_valid:
        product = SEQUENCES[ring.color_sequence.sequence]
    else:
        raise Exception("Product not found.")

    db.clean_up()

    return redirect(GraphQL.create_checkout(product))


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
