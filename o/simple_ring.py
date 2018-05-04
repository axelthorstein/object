from collections import Counter
from profilehooks import timecall

from o.ring import Ring
from o.coordinate import Coordinate
from o.direction import Direction
from o.overlay import Overlay


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

    def create(self):
        """Set all of the dynamic attributes of the Ring.
        """
        self.inner_edges = self.get_inner_edges()
        self.outer_edges = self.get_outer_edges()
        self.inner_radius = self.get_inner_radius()
        self.outer_radius = self.get_outer_radius()
        self.ring_color = self.get_ring_color()
        self.center_color = self.get_center_color()
        self.valid = self.is_valid()

    def is_valid(self):
        """Determine if the ring is valid.

        Returns:
            bool: Whether the ring is valid.
        """
        x, y = 0, 1
        valid = (self.inner_radius < self.outer_radius
                 and self.ring_color != self.center_color
                 and self.inner_edges["left"][x] > self.outer_edges["left"][x]
                 and self.inner_edges["up"][y] < self.outer_edges["up"][y]
                 and self.inner_edges["right"][x] < self.outer_edges["right"][x]
                 and self.inner_edges["down"][y] > self.outer_edges["down"][y])

        return valid

    def get_center_color(self):
        """Find the color inside the circle.

        Return the "highest voted" color from the center. The color with the
        highest combination of frequency and likelihood.

        Returns:
            str: The center color.
        """
        return self.color_freq["inner"].most_common(1)[0][0]

    def get_ring_color(self):
        """Find the color inside the ring.

        Return the "highest voted" color from the ring. The color with the
        highest combination of frequency and likelihood.

        Returns:
            str: The ring color.
        """
        return self.color_freq["outer"].most_common(1)[0][0]

    def get_edge(self, coordinate, starting_coords, direction):
        """Return the edge of the ring.

        Walk from the starting coordinate to in the given direction until an
        edge is found. Then with the coordinates and colors of this edge update
        the attributes of the ring.

        Returns:
            tuple of int: The coordinates of the edge.
        """
        edge_coords = coordinate.move(starting_coords, direction)
        self.update_center_coords(edge_coords)

        return edge_coords

    def get_inner_edge(self, coordinate, directions, direction):
        """Return the inner edge of the ring.

        Args:
            directions (dictionary): Mapping of directions to movement methods.
            depth: The direction to move.

        Returns:
            tuple of int: The coordinates of the inner edge.
        """
        return self.get_edge(coordinate, self.center_coords, directions[direction])
 
    def get_outer_edge(self, coordinate, directions, direction):
        """Return the outer edge of the ring.

        Args:
            directions (dictionary): Mapping of directions to movement methods.
            depth: The direction to move.

        Returns:
            tuple of int: The coordinates of the outer edge.
        """
        starting_coords = directions[direction](self.inner_edges[direction])
        return self.get_edge(coordinate, starting_coords, directions[direction])

    @timecall
    def get_edges(self, get_edge, depth):
        """Return the edges of the ring.

        On each iteration update the value of the center coordinates based on
        the new information from the last edge.

        To find the outer edge we begin moving from the inner edge until
        we reach the original color. We need to increment the inner edge
        by one because it returns the pixel before the color change, so it
        would immeadiately exit otherwise.

        Args:
            get_edge (method): The method for getting edges.
            depth: The inner or outer depth.

        Returns:
            dictionary: The edges.
        """
        edges = {}
        directions = Direction.get_directions()
        coordinate = Coordinate(self.image, depth=depth)

        for direction in directions:
            edges[direction] = get_edge(coordinate, directions, direction)

        self.color_freq[depth] += coordinate.color_freq[depth]

        return edges  

    @timecall
    def get_inner_edges(self):
        """Return the inner edges of the ring.

        Returns:
            dictionary: The inner edges.
        """
        depth = "inner"
        get_edge = self.get_inner_edge

        return self.get_edges(get_edge, depth)

    @timecall
    def get_outer_edges(self):
        """Return the outer edges of the ring.

        Returns:
            dictionary: The outer edges.
        """
        depth = "outer"
        get_edge = self.get_outer_edge

        return self.get_edges(get_edge, depth)

    def get_average_radius(self, edges):
        """Find the average radius from the edges.

        Find which coordinate value is not the same at the center point
        and use it to calculate the average radius.

        Args:
            edges (dictionary): The edges of the ring.

        Returns:
            int: The average radius.
        """
        x, y = 0, 1
        average_radius = 0

        average_radius += abs(self.center_coords[x] - edges["left"][x])
        average_radius += abs(self.center_coords[y] - edges["up"][y])
        average_radius += abs(self.center_coords[y] - edges["down"][y])
        average_radius += abs(self.center_coords[x] - edges["right"][x])

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
