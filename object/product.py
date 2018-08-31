from configs.config import PRODUCT_MAP
from object.detector import Detector
from object.graphql import GraphQL


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
        detector = Detector(
            self.image_path, crop=True, merge_filter=True)
        ring = detector.find_ring(grain=720)

        try:
            return PRODUCT_MAP[ring.color_sequence.sequence]
        except KeyError:
            raise ProductException("Product not found.")
