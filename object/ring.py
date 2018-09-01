from math import hypot

from object.edge import Edge
from object.direction import Direction
from object.overlay import Overlay
from object.color_sequence import ColorSequence
from utils.logging_utils import logger

LOGGER = logger('object')


class Ring:
    """
    A ring based on any number of primary and secondary colored dashes that are
    surrounded inside and outside by the same color.
    """

    def __init__(self, image, center_point, debug=True):
        self.image = image
        self.debug = debug
        self.center_point = center_point
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
        LOGGER.debug('Approximation failed.')
        radius = self.get_radius()

        self.color_sequence = ColorSequence(
            self.image, self.center_point, radius, grain=grain)

    def is_valid(self):
        """Determine if the ring is valid.

        Todo:
            Add real validity check.

        Returns:
            bool: Whether the ring is valid.
        """
        return self.color_sequence.is_valid()

    def get_edges(self):
        """Return the edges around the center point.

        To find the outer edge we begin moving from the inner edge until
        we reach the original color. We need to increment the inner edge
        by one because it returns the pixel before the color change, so it
        would immeadiately exit otherwise.

        Returns:
            Dict[str, Dict[str, Pixel]]: The map of edges around the ring.
        """
        edges = {}
        directions = Direction.get_directions()

        for depth in ['inner', 'outer']:
            edges[depth] = {}

            for direction in directions:
                edge = Edge(self.image, directions[direction])

                if depth == 'inner':
                    pixel = edge.scan(self.center_point)
                else:
                    pixel = edge.scan(edges['inner'][direction])

                edges[depth][direction] = pixel

        self.update_center_coords(edges['inner'])

        return edges

    @staticmethod
    def calculate_distance(inner_point, outer_point):
        """Calculate the distance between two points.

        Args:
            inner_point (Pixel): The inner point.
            outer_point (Pixel): The outer point.

        Returns:
            int: The distance between the points.
        """
        return hypot(inner_point.x - outer_point.x,
                     inner_point.y - outer_point.y)

    def get_radius(self):
        """Return the average radius from the center to the middle of the ring.

        Returns:
            int: The average radius from the center to the middle of the ring.
        """
        # pixel_matrix = self.image.load()

        # pixel_matrix[self.center_point.coords] = (0, 255, 255)
        radii = []
        edges = self.get_edges()
        directions = Direction.get_directions()
        # import pprint
        # pprint.pprint(edges)
        # debug_path = 'images/debug2.png'

        # for point in edges['inner']:
        #     pixel_matrix[edges['inner'][point].coords] = (0, 255, 255)

        # pixel_matrix[self.center_point.coords] = (0, 255, 255)

        # self.image.save(debug_path)

        for direction in directions:
            inner_radius = Ring.calculate_distance(self.center_point,
                                                   edges['inner'][direction])
            outer_radius = Ring.calculate_distance(edges['inner'][direction],
                                                   edges['outer'][direction])

            radii.append(int(inner_radius + (outer_radius / 2)))

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
        return f'color_sequence: {self.color_sequence.sequence}'
