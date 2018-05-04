from collections import Counter
from profilehooks import timecall

from collections import Counter

from o.ring import Ring
from o.move import Move
from o.direction import Direction
from o.overlay import Overlay
from utils.color_utils import update_color_freq, get_highest_color


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
        self.overlay = Overlay(starting_coords)
        self.color_freq = {"inner": Counter(), "outer": Counter()}
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
        valid = (self.inner_radius < self.outer_radius
                 and self.ring_color != self.center_color
                 and self.inner_edges["left"][0] > self.outer_edges["left"][0]
                 and self.inner_edges["up"][1] < self.outer_edges["up"][1]
                 and self.inner_edges["right"][0] < self.outer_edges["right"][0]
                 and self.inner_edges["down"][1] > self.outer_edges["down"][1])
        return valid

    def get_center_color(self):
        """Find the color inside the circle.

        Return the "highest voted" color from the center. The color with the
        highest combination of frequency and likelihood.

        Returns:
            str: The center color.
        """
        return get_highest_color(self.color_freq, "inner")

    def get_ring_color(self):
        """Find the color inside the ring.

        Return the "highest voted" color from the ring. The color with the
        highest combination of frequency and likelihood.

        Returns:
            str: The ring color.
        """
        return get_highest_color(self.color_freq, "outer")

    def get_edge(self, move, starting_coords, direction):
        """Return the edge of the ring.

        Walk from the starting coordinate to in the given direction until an
        edge is found. Then with the coordinates and colors of this edge update
        the attributes of the ring.

        Returns:
            dictionary: The coordinates of the edge.
        """
        edge_coords, color_freq = move.walk(starting_coords, direction)
        self.update_center_coords(edge_coords)
        self.color_freq[move.depth] += color_freq[move.depth]

        return edge_coords

    @timecall
    def get_inner_edges(self):
        """Return the inner edges of the ring.

        On each iteration update the value of the center coordinates based on
        the new information from the last edge.

        Returns:
            dictionary: The inner edges.
        """
        move = Move(self.image, depth="inner")
        left = self.get_edge(move, self.center_coords, Direction.left)
        up = self.get_edge(move, self.center_coords, Direction.up)
        right = self.get_edge(move, self.center_coords, Direction.right)
        down = self.get_edge(move, self.center_coords, Direction.down)

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
            dictionary: The outer edges.
        """
        move = Move(self.image, depth="outer")

        left = self.get_edge(move,
            Direction.left(self.inner_edges["left"]), Direction.left)
        up = self.get_edge(move,
            Direction.up(self.inner_edges["up"]), Direction.up)
        right = self.get_edge(move,
            Direction.right(self.inner_edges["right"]), Direction.right)
        down = self.get_edge(move,
            Direction.down(self.inner_edges["down"]), Direction.down)

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
