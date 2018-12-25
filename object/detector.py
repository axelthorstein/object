#pylint: skip-file

from profilehooks import timecall

from object.coordinate_maps.dashed_ring_map import DashedRingMap
from object.product import Product
from object.product import ProductException
from object.pixel import Pixel
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

    def get_center_variations(self, center_point):
        """Get slight variations of the center point for sampling.

        TODO:
            - Make the transformation functions cleaner.
            - Make the variation equal to .75 of the width of the ring.

        Returns:
            List[Tuples]: The list of varied center points.
        """
        image = self.image.image

        variations = [
            center_point,
            Pixel(image, (int(center_point.x * 0.85), center_point.y)),
            Pixel(image, (center_point.x, int(center_point.y * 0.85))),
            Pixel(image, (int(center_point.x * 1.15), center_point.y)),
            Pixel(image, (center_point.x, int(center_point.y * 1.15)))
        ]

        return variations

    def get_radius_variations(self):
        """Get slight variations of the radius for sampling.

        Returns:
            List[Tuples]: The list of varied radii.
        """
        pass

    def get_product_name(self, center_point):
        """Detect an object in an image and return the corresponding product.

        Args:
            center_point (Pixel): The center point.

        Returns:
            Product: The product.
        """
        coordinates = self.coordinate_map(center_point).coordinates

        if self.debug:
            self.image.draw_ring(coordinates)

        sequence = Sequence(self.image, center_point, coordinates)

        return Product(sequence.color_code).product_name

    @timecall
    def detect_product(self):
        """Detect a product based on the image.

        Returns:
            str: The product name.
        """
        center_points = self.get_center_variations(self.image.center_point)

        for center_point in center_points:
            product_name = self.get_product_name(center_point)

            if product_name:
                return product_name

        raise ProductException("Product not found.")
