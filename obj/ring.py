from math import hypot

from obj.coordinate import Coordinate
from obj.direction import Direction
from obj.overlay import Overlay
from obj.pixel import Pixel
from obj.color_sequence import ColorSequence
from obj.logs import logger

LOGGER = logger('object')


class Ring:
    """
    A ring based on any number of primary and secondary colored dashes that are
    surrounded inside and outside by the same color.
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.debug = debug
        self.center_point = Pixel(image, starting_coords)
        self.radius = 0
        self.color_sequence = None

    def approximate(self, grain):
        """Use the overlay to approximate the color sequence.

        By using the overlays assumed radius of the ring we can potentially
        find the color sequence with minimal calculations. With only the center
        point and the radius we can retrieve the color values for every pixel
        on the circumference.

        Args:
            grain (int): The number of pixels to sample.
        """
        overlay = Overlay(self.center_point)

        self.color_sequence = ColorSequence(
            self.image, overlay.center_point, overlay.radius, grain=grain)

    def calculate(self, grain):
        """Find the edges of the ring to calculate the color sequence.

        If the approximation failed the center point is most likely off, or the
        ring is smaller or larger than we expect by a significant margin. In
        this case scan each direction to find the inner and outer edges of the
        ring and use them to find the average radius. Use the radius to find the
        color sequence.

        Args:
            grain (int): The number of pixels to sample.
        """
        LOGGER.info('Approximation failed.')
        radius = self.get_radius()

        self.color_sequence = ColorSequence(
            self.image, self.center_point, radius, grain=grain)

    def is_valid(self):
        """Determine if the ring is valid.

        Returns:
            bool: Whether the ring is valid.
        """
        # TODO: Add real validity check.
        return self.color_sequence.is_valid

    def get_radius(self):
        """Return the average radius from the center to the middle of the ring.

        To find the outer edge we begin moving from the inner edge until
        we reach the original color. We need to increment the inner edge
        by one because it returns the pixel before the color change, so it
        would immeadiately exit otherwise.

        Returns:
            int: The average radius from the center to the middle of the ring.
        """
        edges = {}
        radii = []
        directions = Direction.get_directions()

        for direction in directions:
            inner_pixel = Coordinate(
                self.image, depth='inner').scan(self.center_point,
                                                directions[direction])
            inner_radius = hypot(self.center_point.x - inner_pixel.x,
                                 self.center_point.y - inner_pixel.y)

            outer_pixel = Coordinate(
                self.image, depth='outer').scan(inner_pixel,
                                                directions[direction])
            outer_radius = hypot(inner_pixel.x - outer_pixel.x,
                                 inner_pixel.y - outer_pixel.y)

            radii.append(int(inner_radius + (outer_radius / 2)))
            edges[direction] = inner_pixel

        self.update_center_coords(edges)

        return sum(radii) / len(radii)

    def update_center_coords(self, inner_edges):
        """Set the center coordinates of the circle.

        Update the ring's center coordinates as the inner edges are found.
        This will provide more accurate results as it progresses.

        Args:
            inner_edges (Tuple[int]): The coordinates of the ring edge.
        """
        x_offset = int((inner_edges['right'].x - inner_edges['left'].x) / 2)
        y_offset = int((inner_edges['down'].y - inner_edges['up'].y) / 2)
        x = inner_edges['left'].x + x_offset
        y = inner_edges['up'].y + y_offset

        self.center_point.update_coords(x, y)

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
        return self.__str__()
