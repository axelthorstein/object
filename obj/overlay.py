from obj.ring import Ring


class Overlay(Ring):
    """
    An object to represent the overlay over the camera.
    """

    def __init__(self, starting_coords):
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
