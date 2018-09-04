from flask import Flask
from flask import render_template
from flask import redirect

from object.graphql import GraphQL
from object.product import Product
from object.product import ProductException
from object.firebase import Firebase
from utils.logging_utils import logger

app = Flask(__name__)

LOGGER = logger('object')


@app.route('/')
def index():
    """Return the view for the image capture page.

    Returns:
        FlaskTemplate: The image capture view.
    """
    return render_template('index.html')


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

    try:
        product = Product(image_path)
    except ProductException as exception:
        return exception.args[0]

    database.clean_up()

    LOGGER.info(product.checkout_url)

    return redirect(product.checkout_url)
