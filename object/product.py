from configs.config import PRODUCT_MAP
from object.detector import Detector
from object.graphql import GraphQL
from utils.logging_utils import logger

LOGGER = logger('object')


class ProductException(Exception):
    pass


class Product:
    """A product."""

    def __init__(self, image_path):
        self.image_path = image_path
        self.product = self.get_product()
        self.checkout_url = GraphQL.create_checkout(self.product)

    def get_product(self):
        """Return the product based on the ring in the image.

        Returns:
            str: The product ID.
        """
        ring = Detector(self.image_path).find_ring()

        LOGGER.info(ring.color_sequence.sequence)

        # if not ring.is_valid():
        #     ring = Detector(self.image_path, merge_filter=True).find_ring()

        # LOGGER.info(ring.color_sequence.sequence)

        if ring.is_valid():
            return PRODUCT_MAP[ring.color_sequence.sequence['code']]

        return "Product not found."
