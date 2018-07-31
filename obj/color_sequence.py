from math import atan2, cos, degrees, sin
from operator import sub
from collections import Counter

from obj.pixel import Pixel
from obj.logs import logger
from utils.color_utils import sequence_to_code
from configs.config import SEQUENCES

LOGGER = logger('object')


class ColorSequence:
    """The sequence of colors in a dashed ring from an image."""

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
        return self.sequence in SEQUENCES

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

    def collapse(self, colors):
        """Collapse the colors into a sequence.

        The numbers of colors in the list will be determined by how many points
        were sampled from the image so we need to collapse them into one color
        per distinct change in color. A distinct change in color is indicated by
        changing from the delimiting color (center color) to a new color and
        back to the delimiting color. The max of each of these groups is taken
        in cause there is a small margin of error in the color identification.
        The end result being a list of one color per dash in the sequence and
        all of the delimiting colors removed.

        Args:
            List[str]: The sequence of colors from the image.

        Returns:
            List[str]: The collapsed sequence of colors.
        """
        # Remove any initial occurances of the center color.

        sequence = []
        j = 0

        try:
            if len(set(colors)) > 1:
                colors = colors[next(
                    colors.index(x)
                    for x in colors
                    if x != self.center_point.colors[0]):]

                for i, color in enumerate(colors):
                    if color == self.center_point.colors[0] or i == len(colors) - 1:
                        if colors[j + 1:i]:
                            sequence.append(Counter(colors[j:i]).most_common(1)[0][0])
                        j = i
        except:
            LOGGER.info("Collapse failed.")

        return sequence

    def calculate_sequence(self):
        """Get the colors from each dash in the ring.

        Get each color from each dash, deduplicating using the center color as
        a delimiter, then removing occurances of the center color.

        Returns:
            str: The integer representation of a color sequence.
        """
        # Get the colors for each pixel on the rings circumference.
        # TODO: Make colors not a list.
        ring_colors = [
            Pixel(self.image, (point)).colors[0] for point in self.points
        ]

        # Collapse duplicates.
        ring_colors = self.collapse(ring_colors)

        # Filter out center color.
        color_sequence = list(
            filter(lambda color: color != self.center_point.colors[0],
                   ring_colors))

        return sequence_to_code(color_sequence)
