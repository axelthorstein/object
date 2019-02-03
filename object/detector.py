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
            Tuple[Pixel]: The list of varied center points.
        """
        image = self.image.image

        variations = [
            center_point,
            Pixel(image, (int(center_point.x * 0.8), center_point.y)),
            Pixel(image, (center_point.x, int(center_point.y * 0.8))),
            Pixel(image, (int(center_point.x * 1.2), center_point.y)),
            Pixel(image, (center_point.x, int(center_point.y * 1.2)))
        ]

        return variations

    def get_radius_variations(self, center_point):
        """Get slight variations of the radius for sampling.

        Returns:
            Tuple[int]: The list of varied radii.
        """
        radius = (center_point.y + center_point.x) * .35

        return (radius, radius * 1.1, radius * 0.8)

    def get_product_name(self, center_point, radius):
        """Detect an object in an image and return the corresponding product.

        Args:
            center_point (Pixel): The center point.
            radius (Pixel): The radius of the circle.

        Returns:
            Product: The product.
        """
        # We want to use the same radius for all rings.
        coordinates = self.coordinate_map(center_point, radius).coordinates
        sequence = Sequence(self.image, center_point, coordinates)

        if self.debug:
            # When this is enabled it will put black pixels on the debug image
            # which will cause the tests to fail if it draws more than one ring.
            self.image.draw_ring(coordinates)

        return Product(sequence).product_name

    @timecall
    def detect_product(self):
        """Detect a product based on the image.

        Returns:
            str: The product name.
        """
        center_points = self.get_center_variations(self.image.center_point)
        radii = self.get_radius_variations(self.image.center_point)

        for center_point in center_points:
            for radius in radii:
                product_name = self.get_product_name(center_point, radius)

                if product_name:
                    return product_name

        raise ProductException("Product not found.")
