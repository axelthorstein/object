import os
import cv2
import matplotlib.image
import numpy as np

# from o.analyzer import Analyzer
from analyzer import Analyzer
import webcolors


class Ring(object):
    """docstring for Ring"""

    def get_center_color(self):
        """Find the color inside the circle.

        Returns:
            str: The center color.
        """
        return self.color(self.center_coords)

    def get_ring_color(self):
        """Find the color inside the ring.

        Returns:
            str: The ring color.
        """
        x = self.center_coords[0] + self.inner_radius + int((self.outer_radius - self.inner_radius) / 2)
        y = self.center_coords[1]

        return self.color((x, y))

    def get_colour_name(rgb):
        """Get the name of a color for a RGB value.

        Resolve the closest human readable name for a RBG value.

        Args:
            rgb (list of int): The Red, Green, Blue triplet.

        Returns:
            str: The color name from the RGB value.
        """
        min_colours = {}

        for key, name in webcolors.css21_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - rgb[0]) ** 2
            gd = (g_c - rgb[1]) ** 2
            bd = (b_c - rgb[2]) ** 2
            min_colours[(rd + gd + bd)] = name

        return min_colours[min(min_colours.keys())]

    def color(self, coords):
        """Return the name of a color for the given pixel.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return Ring.get_colour_name(tuple(self.image[coords[0], coords[1]]))


class SimpleRing(Ring):
    """
    A ring based on the radii and edge points of two circles. This ring bounded by the same color inside and surrounding.

    Using a simple method of linearly analyzing pixels determine if a ring exists in an image. If a ring is found to be in the image, determine the two colors that the ring consists of.

    The description for this simple method can be found here:
    https://gist.github.com/axelthorstein/337312d5030af4b965e5a40271ba0361#simple
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.starting_coords = starting_coords
        self.debug = debug
        self.left_inner_edge = self.walk(starting_coords, SimpleRing.left)
        self.right_inner_edge = self.walk(starting_coords, SimpleRing.right)
        self.up_inner_edge = self.walk(starting_coords, SimpleRing.up)
        self.down_inner_edge = self.walk(starting_coords, SimpleRing.down)
        self.center_coords = self.get_center_coords()
        self.inner_radius = self.get_inner_radius()
        self.outer_radius = self.get_outer_radius()
        self.center_color = self.get_center_color()
        self.ring_color = self.get_ring_color()
        self.is_valid = self.is_valid()

    def is_valid(self):
        """Determine if the ring is valid.

        Returns:
            bool: Whether the ring is valid.
        """
        return self.ring_color != self.center_color

    def get_center_coords(self):
        """Find the center coordinates of the circle.

        Returns:
            int: The center coordinates.
        """
        return (self.get_center_x(), self.get_center_y())

    def get_inner_radius(self):
        """Find the radius of the inner circle.

        Returns:
            int: The inner radius.
        """
        return self.right_inner_edge[0] - self.center_coords[0]

    def get_outer_radius(self):
        """Find the radius of the outer circle.

        Returns:
            int: The outer radius.
        """
        return self.walk(SimpleRing.right(self.right_inner_edge), SimpleRing.right)[0] - self.center_coords[0]

    def get_center_x(self):
        """Find the center x coordinate of the ring based on the inner edges.

        Returns:
            int: The x coordinate of a pixel.
        """
        return int(self.left_inner_edge[0] + ((self.right_inner_edge[0] - self.left_inner_edge[0]) / 2))
        
    def get_center_y(self):
        """Find the center y coordinate of the ring based on the inner edges.

        Returns:
            int: The y coordinate of a pixel.
        """
        return int(self.down_inner_edge[1] + ((self.up_inner_edge[1] - self.down_inner_edge[1]) / 2))

    def up(coords):
        """Increment the y value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0], coords[1] + 1)

    def down(coords):
        """Decrement the y value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0], coords[1] - 1)

    def left(coords):
        """Decrement the x value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0] - 1, coords[1])

    def right(coords):
        """Increment the x value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0] + 1, coords[1])

    def walk(self, starting_coords, direction):
        """Walk a stright line of pixels until a new color is reached.

        Begining at the given stating coordinates continue incrementally in the given direction until a new color is reached. At each new pixel arrived at check the pixels color.
        
        Args:
            starting_coords (tuple of int): The coordinates of the starting pixel.
            direction (method): The direction to increment/decrement.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        starting_color = self.color(starting_coords)
        next_coords = starting_coords
        next_color = self.color(direction(next_coords))

        while next_color == starting_color:
            next_coords = direction(next_coords)
            next_color = self.color(direction(next_coords))

        if self.debug:
            print("Walked {}, starting color: {} at {}, next color: {} at {}".format(direction.__name__, starting_color, starting_coords, next_color, next_coords))

        return next_coords

    def __str__(self):
        """Return a string representation of the ring.

        Returns:
            str: The ring attributes.
        """
        return "".join(["\nRing:\n"
                "  Left inner edge: {}\n".format(self.left_inner_edge),
                "  Right inner edge: {}\n".format(self.right_inner_edge),
                "  Up inner edge: {}\n".format(self.up_inner_edge),
                "  Down inner edge: {}\n".format(self.down_inner_edge),
                "  Center coordinates: {}\n".format(self.center_coords),
                "  Inner radius: {}\n".format(self.inner_radius),
                "  Outer radius: {}\n".format(self.outer_radius),
                "  Center color: {}\n".format(self.center_color),
                "  Ring color: {}\n".format(self.ring_color)
                ])


class HoughTransformRing(Ring):
    """
    A ring object with a center point, and a distance radius to it's inner
    and outer rings.
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.starting_coords = starting_coords
        self.debug = debug
        self.ring_circles = self.get_ring_circles()
        self.inner_circle = self.ring_circles[0]
        self.outer_circle = self.ring_circles[1]
        self.center_coords = self.get_center_coords()
        self.inner_radius = self.get_inner_radius()
        self.outer_radius = self.get_outer_radius()
        self.ring_color = self.get_ring_color()
        self.center_color = self.get_center_color()
        self.is_valid = self.is_valid()

    def get_center_coords(self):
        """Find the center coordinates of the circle.

        Returns:
            int: The center coordinates.
        """
        return (self.inner_circle[0], self.inner_circle[1])

    def get_inner_radius(self):
        """Find the radius of the inner circle.

        Returns:
            int: The inner radius.
        """
        return self.inner_circle[2]

    def get_outer_radius(self):
        """Find the radius of the outer circle.

        Returns:
            int: The outer radius.
        """
        return self.outer_circle[2]

    def get_greyscale_image(image):
        """Convert the image to greyscale.

        Returns:
            np.array of array: The image matrix of pixels.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def is_valid(self):
        """Determine if the ring is valid.
        
        TODO: Add real validity check.

        Returns:
            bool: Whether the ring is valid.
        """
        return (self.outer_circle[2] - self.inner_circle[2]) > 2

    def get_ring_circles(self):
        """Use the Hough Transform algorithm to find candidate circles in the image.

        Returns:
            bool: Whether the ring is valid.
        """
        def round(nums, precision=0):
            return np.uint16(np.around(nums, precision))

        greyscale_image = HoughTransformRing.get_greyscale_image(self.image)

        c1 = round(cv2.HoughCircles(greyscale_image, cv2.HOUGH_GRADIENT, .5, 10, 10, 10, 10, 10)[0][0])
        c2 = round(cv2.HoughCircles(greyscale_image, cv2.HOUGH_GRADIENT, 1.5, 10, 10, 10, 10, 10)[0][0])

        if c1[2] > c2[2]:
            outer_circle = c1
            inner_circle = c2
        else:
            outer_circle = c2
            inner_circle = c1

        if round(inner_circle[0:1], -1) == round(outer_circle[0:1], -1):
            return inner_circle, outer_circle
        raise RingException("The circles found do not share the same center coordinate.")

    def __str__(self):
        """Return a string representation of the ring.

        Returns:
            str: The ring attributes.
        """
        return "".join(["\nRing:\n"
                "  Center coordinates: {}\n".format(self.center_coords),
                "  Inner circle: {}\n".format(self.inner_circle),
                "  Outer circle: {}\n".format(self.outer_circle),
                "  Inner radius: {}\n".format(self.inner_radius),
                "  Outer radius: {}\n".format(self.outer_radius),
                "  Center color: {}\n".format(self.center_color),
                "  Ring color: {}\n".format(self.ring_color)
                ])


class RingException(Exception):
    pass
