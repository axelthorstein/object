from math import atan2, cos, degrees, sin
from itertools import groupby
from operator import sub
from profilehooks import timecall

from obj.pixel import Pixel
from utils.color_utils import sequence_to_code

SEQUENCES = {
    '0000000000000101010101010101010101010101080808080808080808080808080101010101010101010101010000000000':
    'circle_1',
    '020202040404040404080808080808101010101010000000000000010101010101020202':
    'circle_36',
    '020404040808081010100000000101010202':
    'circle_18'
}


class ColorSequence:
    """The sequence of colors in a dashed ring from an image."""

    def __init__(self, image, center_point, radius, grain=360):
        self.image = image
        self.center_point = center_point
        self.radius = radius
        self.grain = grain
        self.sequence = self.calculate_sequence()
        self.is_valid = self.is_valid()

    def is_valid(self):
        """Determine whether the color sequence is valid.

        Check the color sequence generated from the image against all known
        sequences. If the sequence is not known return that is is not valid.

        Returns:
            bool: The validity of the color sequence.
        """
        return self.sequence in SEQUENCES and len(self.sequence) % 18 == 0

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
        lowest_degree = -135
        return sorted(coordinates, key=lambda coord: (lowest_degree - degrees(
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

        # Sort counter clockwise around the center.
        points = self.sort_coordinates(points)

        return points

    @timecall
    def calculate_sequence(self):
        """Get the colors from each dash in the ring.

        Get each color from each dash, deduplicating using the center color as
        a delimiter, then removing occurances of the center color.

        Returns:
            List[str]: The list of colors from each dash.
        """
        points = self.get_points_on_circumference()

        # Get the colors for each pixel on the rings circumference.
        ring_colors = [Pixel(self.image, (point)).colors[0] for point in points]

        # Fold together like elements.
        ring_colors = next(zip(*groupby(ring_colors)))

        # Filter out center color.
        color_sequence = list(
            filter(lambda color: color != self.center_point.colors[0],
                   ring_colors))

        return sequence_to_code(color_sequence)
