import os

from flask import Flask
from flask import render_template

from obj.graphql import GraphQL
from obj.detect import Detect
from obj.config import env
from obj.firebase import Firebase


app = Flask(__name__)


PRODUCT_MAP = {
    "crimson-gold" : "object-001",
}

@app.route('/capture')
def capture():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/cloud_credentials.json"
    return render_template('capture.html')


@app.route('/products')
def get_graphql_products():
    return str(GraphQL.get_products())


@app.route('/checkout/<path:target>')
def create_checkout(target):
    return str(GraphQL.create_checkout(target))


@app.route('/images/<id>', methods=["GET"])
def images(id):
    print("here")
    
    file_path = "images/" + id + ".png"

    db = Firebase(file_path)
    db.download_image()

    # colors = Detect('/Users/axelthor/Projects/object/images/ring.png').detect_circle()
    colors = Detect(file_path).detect_circle()
    color = str(colors[0]) + "-" + str(colors[1])
    if PRODUCT_MAP.get(color):
        product = PRODUCT_MAP[color]
    else:
        product = "object-001"
    print(product)

    db.clean_up()

    return GraphQL.create_checkout(product)['data']['checkoutCreate']['checkout']['webUrl']


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
