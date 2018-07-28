from obj.ring import Ring
from obj.pixel import Pixel


class Overlay(Ring):
    """
    An object to represent the overlay over the camera.
    """

    def __init__(self, image, starting_coords):
        self.center_point = Pixel(image, starting_coords)
        self.inner_radius = self.get_inner_radius()
        self.outer_radius = self.get_outer_radius()
        self.radius = self.get_mid_ring_radius()
        self.inner_edges = self.get_edges(self.inner_radius)
        self.outer_edges = self.get_edges(self.outer_radius)

    def get_inner_radius(self):
        """Return the inner radius of the overlay.

        Returns:
            int: Half the height of the image.
        """
        return int(self.center_point.y * 0.45)

    def get_outer_radius(self):
        """Return the outer radius of the overlay.

        Returns:
            int: The outer radius.
        """
        return int(self.center_point.y * 0.22)

    def get_mid_ring_radius(self):
        """Find the radius of the middle of the outer circle.

        Returns:
            int: The average radius.
        """
        return int(self.inner_radius + (self.outer_radius / 2))

    def get_edges(self, radius):
        """Return the edges of the overlay.

        Returns:
            int: The edges.
        """
        center = self.center_point
        edges = {
            "left": (center.x - radius, center.y),
            "up": (center.x, center.y + radius),
            "right": (center.x + radius, center.y),
            "down": (center.x, center.y - radius)
        }

        return edges

    def __str__(self):
        """Return a description of the Pixel.

        Returns:
            str: The string representation of the Pixel.
        """
        return f'Overlay {self.center_point} with {self.radius} radius.'

    def __repr__(self):
        desc = f'\n{self.__class__.__name__}:\n'

        for attribute in self.__dict__:
            key = attribute.replace('_', ' ').capitalize()
            desc += f'    {key}: {self.__dict__[attribute]},\n'

        return desc
