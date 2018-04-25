import os
import cv2
import matplotlib.image
import numpy as np

# from o.analyzer import Analyzer
from analyzer import Analyzer
import webcolors


class HoughTransformRing:
    """
    A ring object with a center point, and a distance radius to it's inner
    and outer rings.
    """

    def __init__(self, image, image_path):
        self.image = image
        self.image_path = image_path
        self.ring_circles = self.get_ring_circles()
        self.inner_circle = self.ring_circles[0]
        self.outer_circle = self.ring_circles[1]
        self.center_coords = (inner_circle[0], inner_circle[1])
        self.inner_radius = inner_circle[2]
        self.outer_radius = outer_circle[2]
        self.is_ring = (outer_circle[2] - inner_circle[2]) > 2
        self.colors = self.get_colors()[0]
        self.center_color = self.colors[0]
        self.ring_color = self.colors[1]

    def get_ring_circles(self):

        def round(nums, precision=0):
            return np.uint16(np.around(nums, precision))

        # print(cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, .5, 20, 30, 30, 10, 10))

        c1 = HoughTransformRing.round(cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, .5, 10, 10, 10, 10, 10)[0][0])
        c2 = round(cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.5, 10, 10, 10, 10, 10)[0][0])

        if c1[2] > c2[2]:
            outer_circle = c1
            inner_circle = c2
        else:
            outer_circle = c2
            inner_circle = c1

        if round(inner_circle[0:1], -1) == round(outer_circle[0:1], -1):
            return inner_circle, outer_circle

    def get_rgb(self, rgb):
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def get_secondary_color(self, image, primary_color):
        """
        The while will go out of bounds if the ring is too close to the top.
        """
        if self.is_ring:
            secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1]]))
        else:
            offset = self.outer_radius + 1
            secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1] + offset]))

            while secondary_color == primary_color:
                offset += 10
                secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1] + offset]))

        return secondary_color

    def get_rgb_coords(self):
        if self.is_ring:
            return (self.center_coords[0], ((self.outer_radius - self.inner_radius) // 2)
                    + self.inner_radius + self.center_coords[1])
        else:
            return (self.center_coords[0], self.inner_radius // 2 + self.center_coords[1])

    def get_colors(self):
        image = matplotlib.image.imread(self.image_path)

        rgb_coords = self.get_rgb_coords()

        primary_color = Analyzer.get_color(self.get_rgb(image[rgb_coords[0]][rgb_coords[1]]))
        secondary_color = self.get_secondary_color(image, primary_color)
        
        return (primary_color, secondary_color)

    def to_string(self):
        return "Detected a ring at the coordinates {} with a inner and \
outer radius of {} from {}.".format(
               self.center_coords, (self.inner_radius, self.outer_radius),
               os.path.basename(self.image_path).replace("_cropped.png", ""))


class SimpleRing:
    """
    A ring based on the radii and edge points of two circles. This ring bounded by the same color inside and surrounding.

    Using a simple method of linearly analyzing pixels determine if a ring exists in an image. If a ring is found to be in the image, determine the two colors that the ring consists of.

    The description for this simple method can be found here:
    https://gist.github.com/axelthorstein/337312d5030af4b965e5a40271ba0361#simple
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.debug = debug
        self.left_inner_edge = self.walk(starting_coords, SimpleRing.left)
        self.right_inner_edge = self.walk(starting_coords, SimpleRing.right)
        self.up_inner_edge = self.walk(starting_coords, SimpleRing.up)
        self.down_inner_edge = self.walk(starting_coords, SimpleRing.down)
        self.center_coords = (self.get_center_x(), self.get_center_y())
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
        return SimpleRing.get_colour_name(tuple(self.image[coords[0], coords[1]]))

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
