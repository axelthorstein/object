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
        super(Product, self).__init__()
        self.image_path = image_path
        self.product = self.get_product()
        self.checkout_url = GraphQL.create_checkout(self.product)

    def get_product(self):
        """Return the product based on the ring in the image.

        Returns:
            str: The product ID.
        """
        detector = Detector(self.image_path)
        ring = detector.find_ring()
        sequence = 'ColorSequence: {}'.format(ring.color_sequence.sequence)

        LOGGER.info(sequence)

        if ring.color_sequence.sequence['code'] not in PRODUCT_MAP:
            detector = Detector(self.image_path, merge_filter=True)
            ring = detector.find_ring()

        sequence = 'ColorSequence: {}'.format(ring.color_sequence.sequence)
        LOGGER.info(sequence)

        try:
            return PRODUCT_MAP[ring.color_sequence.sequence['code']]
        except KeyError:
            raise ProductException("Product not found.")
