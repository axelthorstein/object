from math import atan2, cos, degrees, sin
from operator import sub

from object.pixel import Pixel
from object.logs import logger
from utils.color_utils import sequence_to_code
from utils.list_utils import collapse
from configs.config import PRODUCT_MAP

LOGGER = logger('object')


class ColorSequence:
    """The sequence of colors in a ring from an image."""

    def __init__(self, image, center_point, radius, grain):
        self.image = image
        self.center_point = center_point
        self.radius = radius
        self.grain = grain
        self.points = self.get_points_on_circumference()
        self.sequence = self.calculate_sequence()
        self.is_valid = self.is_valid()

    def is_valid(self):
        """Determine whether the color sequence is valid.

        Check the color sequence generated from the image against all known
        sequences. If the sequence is not known return that is is not valid.

        TODO: Add back `and len(self.sequence) % 18 == 0` check.

        Returns:
            bool: The validity of the color sequence.
        """
        return self.sequence in PRODUCT_MAP

    def sort_coordinates(self, coordinates):
        """Sort the coordinates counter clockwise around the center.

        The coordinates need to be sorted so that they are in order of how they
        appear arround the center so that we can get an accurate ordering of
        colors in the dashes.

        Implementation from Stack Overflow commnent:
        https://stackoverflow.com/questions/51074984/
        sorting-according-to-clockwise-point-coordinates/51075419

        "On second thought that actually won't work, since for every coordinate
        on the list there's always another coordinate whose vector to the
        centroid is clockwise to that of the said coordinate, so there will be
        no "bottom" to the comparison. In OP's case, we need -135 degrees to be
        the "bottom" of the sorted list of coordinates. The sign of the 2D
        cross-product can only help determine if one vector is clockwise to
        another but cannot help establish how far away from the "bottom"
        (i.e. -135 degrees) a vector is."

        Args:
            coordinates (List[Tuple[int, int]]): The ring coordinates.

        Returns:
            List[Tuple[int, int]]: The sorted coordinates.
        """
        leftmost_degree = 180
        return sorted(coordinates, key=lambda coord: (leftmost_degree - degrees(
            atan2(*tuple(map(sub, coord, self.center_point.coords))[::-1]))) % 360)

    def get_points_on_circumference(self):
        """Find all the points on the circumference on the ring.

        Increasing the grain will potentially increase accuracy, but will be
        negligable beyond a certain point and will also increase runtime.

        Returns:
            List[Tuple[int, int]]: The sorted points on the circumference of the circle.
        """
        points = []

        for point in range(self.grain):
            x = int(self.radius * cos(point) + self.center_point.x)
            y = int(self.radius * sin(point) + self.center_point.y)

            points.append((x, y))

        # Deduplicate.
        points = list(set(points))

        # Sort counter clockwise around the center.
        points = self.sort_coordinates(points)

        return points

    def calculate_sequence(self):
        """Get the colors from each dash in the ring.

        Get each color from each dash, deduplicating using the center color as
        a delimiter, then removing occurances of the center color.

        Returns:
            str: The integer representation of a color sequence.
        """
        # Get the colors for each pixel on the rings circumference.
        ring_colors = [Pixel(self.image, point).color for point in self.points]

        # Collapse duplicates.
        color_sequence = collapse(ring_colors, self.center_point.color)

        return sequence_to_code(color_sequence)
