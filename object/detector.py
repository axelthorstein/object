#pylint: skip-file

from profilehooks import timecall

from object.coordinate_maps.dashed_ring_map import DashedRingMap
from object.product import Product
from object.sequence import Sequence
from utils.logging_utils import logger

LOGGER = logger('object')


class Detector:
    """
    Detect an object from a given image.
    """

    def __init__(self, image, coordinate_map=DashedRingMap, debug=False):
        self.image = image
        self.coordinate_map = coordinate_map
        self.debug = debug

    def get_product(self, center_point):
        """Detect an object in an image and return the corresponding product.

        Args:
            center_point (Pixel): The center point.

        Returns:
            Product: The product.
        """
        coordinates = self.coordinate_map(center_point).coordinates
        sequence = Sequence(self.image, center_point, coordinates)

        if self.debug:
            self.image.draw_ring(coordinates)

        return Product(sequence.color_code)

    @timecall
    def detect_product(self):
        """Detect a product based on the image.

        Returns:
            str: The product name.
        """
        center_point = self.image.center_point
        product = self.get_product(center_point)

        while not product.is_valid():
            center_point = self.image.center_point
            product = self.get_product(center_point)

        return product.get_name()
