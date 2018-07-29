from collections import Counter

from obj.pixel import Pixel
from obj.direction import Direction
from utils.color_utils import update_color_freq


class Coordinate:
    """
    An interface for incrementing coordinates in a pixel matrix.
    """

    def __init__(self, image, depth, color_range='css2'):
        self.image = image
        self.depth = depth
        self.color_range = color_range
        self.color_freq = {"inner": Counter(), "outer": Counter()}

    def probe_adjacent_pixel(self, coords, direction, steps, starting_colors):
        """Probe the two adjacent pixels if the first pixel returns a new color.

        Check the two pixels beside the pixel that was just checked to see
        if the edge is increasing or decreasing on an angle that is less than
        45 degrees.

        TODO: May need to return the original direciton pixel so it doesn't
        always veer off to certain direction.

        Args:
            coords (Tuple[int, int]): The original coordinates of the pixel.
            direction (Direction): The direction that was being checked.
            steps (int): How many pixels to increment/decrement.
            starting_colors (List[str]): The original colors to check against.

        Returns:
            Pixel: The pixel to move to.
        """
        adjacent_directions = Direction.get_adjacent_direction(direction)

        for adjacent_direction in adjacent_directions:
            pixel = Pixel(self.image, coords)
            pixel.move(adjacent_direction, steps)

            if pixel.colors_intersect(starting_colors):
                return pixel

        return pixel

    def move(self, starting_coords, direction, steps):
        """Walk a stright line of pixels until a new color is reached.

        Begining at the starting coordinates continue incrementally
        in the given direction until a new color is reached. At each new
        pixel arrived at check the pixels color. Given that the color name
        detection can be unreliable we need to get the three most likely colors
        and compare against the three most likely starting colors. If there are
        no common elements for two iterations we consider an edge to be found
        and exit. This provides us with minimal error recovery.

        Args:
            starting_coords (Tuple[int, int]): Coordinates of the starting pixel.
            direction (method): Direction to increment/decrement.
            steps (int): The amount of pixels to skew on each interation.

        Returns:
            Tuple[int, int]: The coordinates of a pixel.
        """
        starting_colors = Pixel(self.image, starting_coords).colors
        pixel = Pixel(self.image, starting_coords)

        while pixel.colors_intersect(
                starting_colors) and not pixel.out_of_bounds():
            update_color_freq(self.color_freq, pixel.colors, self.depth)

            pixel.move(direction, steps)

            if self.depth == 'outer':
                if not pixel.colors_intersect(starting_colors):
                    pixel = self.probe_adjacent_pixel(pixel.coords, direction,
                                                      steps, starting_colors)

        return pixel

    @staticmethod
    def side_step(rows_checked, direction):
        """Move to a perpendicular row to the one that was just checked.

        Alternate the direction to move to based on the number of rows that
        have been checked so far.

        Args:
            rows_checked (int): The number of rows checked.
            direction (method): Direction to increment/decrement.

        Returns:
            Direction: The perpendicular direction to move to.
        """
        if direction in [Direction.left, Direction.right]:
            if rows_checked % 2 == 0:
                return Direction.up
            return Direction.down
        if rows_checked % 2 == 0:
            return Direction.left
        return Direction.right

    def probe(self, starting_coords, direction, steps=1):
        """Probe the direction until part of the ring is found.

        In some cases we may not have a fully formed ring, so in order to
        determine where the ring begins we need to check along a line of pixels
        and if not part of the ring is found, we skew slightly and try again.
        Continue checking until an edge is found.

        TODO: We may need to have a limit to the number of rows checked.

        Args:
            starting_coords (Tuple[int, int]): Coordinates of the starting pixel.
            direction (method): Direction to increment/decrement.
            steps (int): The amount of pixels to skew on each interation.

        Returns:
            Tuple[int, int]: The coordinates of a pixel.
        """
        rows_checked = 0
        pixel = self.move(starting_coords, direction, steps)
        step_direction = Coordinate.side_step(rows_checked, direction)

        while pixel.out_of_bounds():
            starting_coords = step_direction(
                starting_coords, steps=rows_checked)
            pixel = self.move(starting_coords, direction, steps)
            step_direction = Coordinate.side_step(rows_checked, direction)
            rows_checked += 1

        return pixel
