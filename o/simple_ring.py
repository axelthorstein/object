from collections import Counter
from operator import itemgetter
from profilehooks import timecall

from o.ring import Ring
from o.move import Move
from o.overlay import Overlay
from utils.color_utils import get_color, update_color_freq


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
