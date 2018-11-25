from object.coordinate_maps.dashed_ring_map import DashedRingMap
from object.sequence import Sequence
from utils.logging_utils import logger
from configs.config import PRODUCT_MAP

LOGGER = logger('object')


class Object:
    """A coordinate map applied to an image to identify a product."""

    def __init__(self, image, center_point, radius):
        self.image = image
        self.center_point = center_point
        self.radius = radius
        self.sequence = None

    def approximate(self, grain):
        """Approximate the sequence of an object.

        By using the overlays assumed radius of the object we can potentially
        find the sequence with minimal calculations. With only the center
        point and the radius we can retrieve the values for every pixel.

        Args:
            grain (int): The number of pixels to sample.
        """
        coordinates = DashedRingMap(self.center_point, self.radius,
                                    grain).coordinates
        self.sequence = Sequence(self.image, self.center_point, coordinates)

    def is_valid(self):
        """Determine whether the sequence is valid.

        Check every rotation of the coded sequence to see if it exists in the
        product map.

        Returns:
            bool: The validity of the sequence.
        """
        code = self.sequence.sequence['code']

        if code in PRODUCT_MAP:
            return True

        for _ in code:
            code = code[1:] + code[0]

            if code in PRODUCT_MAP:
                return True

        return False

    def __str__(self):
        """Return a description of the ring.

        Returns:
            str: The string representation of the ring.
        """
        desc = f'\n{self.__class__.__name__}:\n'

        for attribute in self.__dict__:
            key = attribute.replace('_', ' ').capitalize()
            desc += f'    {key}: {self.__dict__[attribute]},\n'

        return desc

    def __repr__(self):
        """Return a description of the ring.

        Returns:
            str: The string representation of the ring.
        """
        return f'sequence: {self.sequence.sequence}'
