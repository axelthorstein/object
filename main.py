import os

from flask import Flask
from flask import render_template
from flask import redirect

from object.graphql import GraphQL
from object.product import Product
from object.firebase import Firebase

app = Flask(__name__)


@app.route('/')
def index():
    """Return the OK status code.

    Returns:
        str: The OK status code.
    """
    return "200"


@app.route('/capture')
def capture():
    """Return the view for the image capture page.

    Returns:
        FlaskTemplate: The image capture view.
    """
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "configs/cloud_credentials.json"
    return render_template('capture.html')


@app.route('/products')
def get_graphql_products():
    """A GraphQL endpoint to return a list of products.

    Returns:
        str: The list of products.
    """
    return str(GraphQL.get_products())


def download_image(image_path):
    """Download the image from Firebase

    Args:
        image_path (str): The remote path to the image.

    Returns:
        Firebase: The Firebase database reference.
    """
    database = Firebase(image_path)
    database.download_image()

    return database


@app.route('/images/<product_id>', methods=["GET"])
def get_product(product_id):
    """A GraphQL endpoint to return a Shopify checkout URL for a given product.

    Returns:
        str: The product checkout URL.
    """
    image_path = "images/" + product_id + ".png"

    database = download_image(image_path)
    product = Product(image_path)
    database.clean_up()

    return redirect(product.checkout_url)
