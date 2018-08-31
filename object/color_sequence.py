from math import atan2, cos, degrees, sin
from operator import sub

from object.pixel import Pixel
from utils.logging_utils import logger
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

    @staticmethod
    def are_rotations(string1, string2):
        """Check if strings are rotations of each other.

        You can tell if a string is a rotated version of another string if it's
        inside a duplicated version of the first string.

        Examples:
            >>> s1 = "abcd"
            >>> s2 = "cdab"
            >>> "cdab" in "abcdabcd"
            True

        Args:
            string1 (str): String to check against.
            string2 (str): String to check against.

        Returns:
            str: The product code string if they are rotations of each other.
        """
        if len(string1) == len(string2) and string2 in string1 + string1:
            return string2

        return ""

    def is_valid(self):
        """Determine whether the color sequence is valid.

        Check the color sequence generated from the image against all known
        sequences. If the sequence is not known return that is is not valid.
        The first check will be O(1), but if the sequence is known, but we've
        only seen a rotated version then we need to check for the rotated
        version in each key of the product map which is O(n). Another solution
        would be to put every variation of a roation for a color sequence in the
        color map so that it would always be O(1), but that means the product
        map could become enormous.

        TODO: Add back `and len(self.sequence) % 18 == 0` check.

        Returns:
            bool: The validity of the color sequence.
        """
        if self.sequence['code'] in PRODUCT_MAP:
            return True

        for product_sequence in PRODUCT_MAP:
            if ColorSequence.are_rotations(self.sequence['code'],
                                           product_sequence):
                # If we have found a rotated version of our sequence in the
                # product map, we'll need to update to that order so we can pull
                # the product later.
                self.sequence['code'] = product_sequence
                return True

        return False

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

        return {
            "code": sequence_to_code(color_sequence),
            "colors": color_sequence
        }
