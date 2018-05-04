from collections import Counter

from o.direction import Direction
from utils.color_utils import get_color, update_color_freq


class Coordinate:
    """
    An interface for incrementing coordinates in a pixel matrix.
    """

    def __init__(self, image, depth):
        self.image = image
        self.depth = depth

    def get_pixel(self, coords):
        """Get the pixel at the given coordinate.
        
        Args:
            coords (tuple of int): The coordinates of the pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return get_color(self.image.getpixel(coords))

    def move(self, starting_coords, direction):
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
        current_colors = self.get_pixel(direction(current_coords))
        last_failed = False
        color_freq = {"inner": Counter(), "outer": Counter()}

        # compare the three most likely colors against the three starting colors
        # because the color identification can be unreliable
        while bool(starting_colors & current_colors) or last_failed == False:

            # checking if the last iteration failed provides a small error
            # recovery scheme in case we find a single unrepresentative pixel
            if bool(starting_colors & current_colors):
                last_failed = True
            else:
                last_failed = False

            # track color frequency
            color_freq = update_color_freq(color_freq, current_colors, self.depth)

            # increment and update the current values
            current_coords = direction(current_coords)
            current_colors = self.get_pixel(current_coords)

        return current_coords, color_freq
