from collections import Counter

from obj.direction import Direction
from utils.color_utils import get_color, get_most_likely_colors, update_color_freq


class Coordinate:
    """
    An interface for incrementing coordinates in a pixel matrix.
    """

    def __init__(self, image, depth, confidence='high'):
        self.image = image
        self.depth = depth
        self.confidence = confidence
        self.color_freq = {"inner": Counter(), "outer": Counter()}



    def move(self, starting_coords, direction, jump=1):
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

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        # get all the starting values
        starting_colors = self.get_pixel_colors(direction(starting_coords))
        current_coords = direction(starting_coords, jump=jump)
        current_colors = self.get_pixel_colors(current_coords)
        last_failed = False

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
            update_color_freq(self.color_freq, current_colors, self.depth)

            # increment and update the current values
            current_coords = direction(current_coords)
            current_colors = self.get_pixel_colors(current_coords)

            # Return if we have reached the end of the image.
            # TODO: Add max pixel range.
            if (((starting_coords[0] * 2 - jump) <= current_coords[0]) or
                (current_coords[0] <= jump) or
                ((starting_coords[1] * 2 - jump) <= current_coords[1]) or
                (current_coords[1] <= jump)):
                return current_coords

        return current_coords

    def side_step(self, iteration, direction):
        """

        """

        if direction in [Direction.left, Direction.right]:
            if iteration % 2 == 1:
                return Direction.up
            else:
                return Direction.down
        else:
            if iteration % 2 == 1:
                return Direction.left
            else:
                return Direction.right


    def probe(self, starting_coords, direction, jump=2):
        """Probe the direction until part of the ring is found.

        In some cases we may not have a fully formed ring, so in order to
        determine where the ring begins we need to check along a line of pixels
        and if not part of the ring is found, we skew slightly and try again.
        check up to (10 * jump) rows of pixels for a colored pixel that isn't
        the same color as the center.

        Args:
            starting_coords (tuple of int): Coordinates of the starting pixel.
            direction (method): Direction to increment/decrement.
            jump (int): The amount of pixels to skew on each interation.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        iteration = 0
        current_coords = self.move(starting_coords, direction)
        center_color = self.get_pixel_colors(starting_coords)
        current_color = center_color
        step_direction = self.side_step(iteration, direction)

        while center_color == current_color:
            starting_coords = step_direction(starting_coords, iteration)

            current_coords = self.move(starting_coords, direction)
            current_color = self.get_pixel_colors(current_coords)
            step_direction = self.side_step(iteration, direction)
            iteration += jump
            print(current_coords, direction, step_direction, iteration)

        return current_coords

