import cv2
import numpy as np
from collections import Counter
from operator import itemgetter
from profilehooks import timecall

from o.analyzer import Analyzer
from utils.color_utils import get_color, update_color_freq
from o.move import Move

class Ring(object):
    """
    An abstract Ring object.
    """

    @staticmethod
    def format_edges(edges):
        """Return a string representation of the overlays edges.

        Returns:
            str: The overlay edges.
        """
        return "".join(["\n"
                "    Left coordinates:  {}\n".format(edges["left"]),
                "    Up coordinates:    {}\n".format(edges["up"]),
                "    Right coordinates: {}\n".format(edges["right"]),
                "    Down coordinates:  {}".format(edges["down"])
                ])


class Overlay(Ring):
    """
    An object to represent the overlay over the camera.
    """

    def __init__(self, image, starting_coords):
        self.image = image
        self.center_coords = starting_coords
        self.inner_radius = self.get_inner_radius()
        self.outer_radius = self.get_outer_radius()
        self.inner_edges = self.get_inner_edges()
        self.outer_edges = self.get_outer_edges()

    def get_inner_radius(self):
        """Return the inner radius of the overlay.

        Returns:
            int: Half the height of the image.
        """
        return int(self.center_coords[1] * 0.27)

    def get_outer_radius(self):
        """Return the outer radius of the overlay.

        Returns:
            int: The outer radius.
        """
        return int(self.center_coords[1] * 0.45)

    def get_inner_edges(self):
        """Return the inner edges of the overlay.

        Returns:
            int: The inner edges.
        """
        center = self.center_coords
        inner_edges = {
            "left": (center[0] - self.inner_radius, center[1]),
            "up": (center[0], center[1] + self.inner_radius),
            "right": (center[0] + self.inner_radius, center[1]),
            "down": (center[0], center[1] - self.inner_radius)
        }

        return inner_edges

    def get_outer_edges(self):
        """Return the outer edges of the overlay.

        Returns:
            int: The outer edges.
        """
        center = self.center_coords
        outer_edges = {
            "left": (center[0] - self.outer_radius, center[1]),
            "up": (center[0], center[1] + self.outer_radius),
            "right": (center[0] + self.outer_radius, center[1]),
            "down": (center[0], center[1] - self.outer_radius)
        }

        return outer_edges

    def __str__(self):
        """Return a string representation of the overlay.

        Returns:
            str: The overlay attributes.
        """
        return "".join(["\nOverlay:\n"
                "  Center coordinates: {}\n".format(self.center_coords),
                "  Inner radius: {}\n".format(self.inner_radius),
                "  Outer radius: {}\n".format(self.outer_radius),      
                "  Inner edges: {}\n".format(
                    Ring.format_edges(self.inner_edges)),
                "  Outer edges: {}\n".format(
                    Ring.format_edges(self.outer_edges))
                ])

class SimpleRing(Ring):
    """
    A ring based on the radii and edge points of two circles. This ring
    bounded by the same color inside and surrounding.

    Using a simple method of linearly analyzing pixels determine if a
    ring exists in an image. If a ring is found to be in the image,
    determine the two colors that the ring consists of.

    The description for this simple method can be found here:
    https://gist.github.com/axelthorstein/337312d5030af4b965e5a40271ba0361
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.debug = debug
        self.center_coords = starting_coords
        self.overlay = Overlay(image, starting_coords)
        self.color_freq = {"inner": {}, "outer": {}}
        self.inner_edges = self.get_inner_edges()
        self.outer_edges = self.get_outer_edges()
        self.inner_radius = self.get_inner_radius()
        self.outer_radius = self.get_outer_radius()
        self.ring_color = self.get_ring_color()
        self.center_color = self.get_center_color()
        self.is_valid = self.is_valid()

    def is_valid(self):
        """Determine if the ring is valid.

        Returns:
            bool: Whether the ring is valid.
        """
        return self.ring_color != self.center_color

    def get_center_color(self):
        """Find the color inside the circle.

        Return the "highest voted" color from the center. The color with the
        highest combination of frequency and likelihood.

        Returns:
            str: The center color.
        """
        return max(dict(self.color_freq["inner"]).items(), key=itemgetter(1))[0]

    def get_ring_color(self):
        """Find the color inside the ring.

        Return the "highest voted" color from the ring. The color with the
        highest combination of frequency and likelihood.

        Returns:
            str: The ring color.
        """
        return max(dict(self.color_freq["outer"]).items(), key=itemgetter(1))[0]

    @timecall
    def get_inner_edges(self):
        """Return the inner edges of the ring.

        Returns:
            int: The inner edges.
        """
        left = self.walk(self.center_coords, Move.left, depth="inner")
        up = self.walk(self.center_coords, Move.up, depth="inner")
        right = self.walk(self.center_coords, Move.right, depth="inner")
        down = self.walk(self.center_coords, Move.down, depth="inner")

        inner_edges = {
            "left": left,
            "up": up,
            "right": right,
            "down": down
        }

        return inner_edges

    @timecall
    def get_outer_edges(self):
        """Return the outer edges of the ring.

        To find the outer edge we begin walking from the inner edge until
        we reach the original color. We need to increment the inner edge
        by one because it returns the pixel before the color change, so it
        would immeadiately exit otherwise.

        Returns:
            int: The outer edges.
        """
        left = self.walk(Move.left(self.inner_edges["left"]),
           Move.left, depth="outer")
        up = self.walk(Move.up(self.inner_edges["up"]),
           Move.up, depth="outer")
        right = self.walk(Move.right(self.inner_edges["right"]),
           Move.right, depth="outer")
        down = self.walk(Move.down(self.inner_edges["down"]),
           Move.down, depth="outer")

        outer_edges = {
            "left": left,
            "up": up,
            "right": right,
            "down": down
        }

        return outer_edges

    def get_average_radius(self, edges):
        """Find the average radius from the edges.

        Find which coordinate value is not the same at the center point
        and use it to calculate the average radius.

        Args:
            edges (dictionary): The edges of the ring.
        Returns:
            int: The average radius.
        """
        average_radius = 0

        average_radius += abs(self.center_coords[0] - edges["left"][0])
        average_radius += abs(self.center_coords[1] - edges["up"][1])
        average_radius += abs(self.center_coords[1] - edges["down"][1])
        average_radius += abs(self.center_coords[0] - edges["right"][0])

        return int(average_radius / 4)

    def get_inner_radius(self):
        """Find the radius of the inner circle.

        Returns:
            int: The inner radius.
        """
        return self.get_average_radius(self.inner_edges)

    def get_outer_radius(self):
        """Find the radius of the outer circle.

        Returns:
            int: The outer radius.
        """
        return self.get_average_radius(self.outer_edges)

    def update_center_coords(self, coords):
        """Set the center coordinates of the circle.

        Update the ring's center coordinates as the inner edges are found.
        This will provide more accurate results as it progresses.

        Args:
            coords (tuple of int): The coordinates of the ring edge.
        """
        x, y = 0, 1

        center = self.center_coords
        overlay_radius = self.overlay.inner_radius        

        # we are updating the y coordinate (up | down)
        if center[x] == coords[x]:
            # get the distance between the center and the inner edge minus
            # the overlay radius. Update the center to be closer to the true
            # center
            if center[y] > coords[y]:
                offset = overlay_radius - abs(center[y] - coords[y])
            else:
                offset = abs(center[y] - coords[y]) - overlay_radius
            self.center_coords = (center[x], center[y] + offset)

        # we are updating the x coordinate (left | right)
        else:
            if center[x] > coords[x]:
                offset = overlay_radius - abs(center[x] - coords[x])
            else:
                offset = abs(center[x] - coords[x]) - overlay_radius
            self.center_coords = (center[x] + offset, center[y])

    def get_pixel(self, coords):
        """Get the pixel at the given coordinate.
        
        Args:
            coords (tuple of int): The coordinates of the pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return get_color(self.image.getpixel(coords))

    def walk(self, starting_coords, direction, depth=True):
        """Walk a stright line of pixels until a new color is reached.

        Begining at the starting coordinates continue incrementally
        in the given direction until a new color is reached. At each new
        pixel arrived at check the pixels color. Given that the color name
        detection can be unreliable we need to get the three most likely colors
        and compare against the three most likely starting colors. If there are
        no common elements for two iterations we consider an edge to be found
        and exit. This provides us with minimal error recovery.
        
        Args:
            starting_coords (tuple of int): Coordinates of the starting pixel.
            direction (method): Direction to increment/decrement.
            depth (str): Whether this is for inner or outer colours.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        # advance one past just to be safe and away from the edge
        starting_coords = direction(starting_coords)

        # get all the starting values
        starting_colors = self.get_pixel(starting_coords)
        current_coords = starting_coords
        next_colors = self.get_pixel(direction(current_coords))
        last_failed = False

        # compare the three most likely colors against the three starting colors
        # because the color identification can be unreliable
        while bool(starting_colors & next_colors) or last_failed == False:

            # checking if the last iteration failed provides a small error
            # recovery scheme in case we find a single unrepresentative pixel
            if bool(starting_colors & next_colors):
                last_failed = True
            else:
                last_failed = False

            # track color frequency
            self.color_freq = update_color_freq(self.color_freq, next_colors, depth)

            # increment and update the next values
            current_coords = direction(current_coords)
            next_colors = self.get_pixel(current_coords)

        # update the value of the center coordinates based on the new
        # information we have found
        if depth == "inner":
            self.update_center_coords(current_coords)

        return current_coords

    def __str__(self):
        """Return a string representation of the ring.

        Returns:
            str: The ring attributes.
        """
        return "".join(["\nRing:\n"
                "  Center coordinates: {}\n".format(self.center_coords),
                "  Inner radius: {}\n".format(self.inner_radius),
                "  Outer radius: {}\n".format(self.outer_radius),
                "  Inner edges: {}\n".format(
                    Ring.format_edges(self.inner_edges)),
                "  Outer edges: {}\n".format(
                    Ring.format_edges(self.outer_edges)),
                "  Center color: {}\n".format(self.center_color),
                "  Ring color:   {}\n".format(self.ring_color),
                ])


class HoughTransformRing(Ring):
    """
    A ring object with a center point, and a distance radius to it's inner
    and outer rings.
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
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
        """Use the Hough Transform algorithm to find circles in the image.

        Returns:
            bool: Whether the ring is valid.
        """
        def round(nums, precision=0):
            return np.uint16(np.around(nums, precision))

        greyscale_image = HoughTransformRing.get_greyscale_image(self.image)

        c1 = round(cv2.HoughCircles(
            greyscale_image, cv2.HOUGH_GRADIENT, .5, 10, 10, 10, 10, 10)[0][0]
        )
        c2 = round(cv2.HoughCircles(
            greyscale_image, cv2.HOUGH_GRADIENT, 1.5, 10, 10, 10, 10, 10)[0][0]
        )

        if c1[2] > c2[2]:
            outer_circle = c1
            inner_circle = c2
        else:
            outer_circle = c2
            inner_circle = c1

        if round(inner_circle[0:1], -1) == round(outer_circle[0:1], -1):
            return inner_circle, outer_circle
        raise RingException("The circles have different center coordinates.")

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
                "  Ring color:   {}\n".format(self.ring_color)
                ])


class RingException(Exception):
    pass
