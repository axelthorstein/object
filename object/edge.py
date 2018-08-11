from object.pixel import Pixel
from object.direction import Direction


class Edge:
    """
    An interface for finding the next edge from a starting pixel.
    """

    def __init__(self, image, direction, depth):
        self.image = image
        self.direction = direction
        self.depth = depth

    def scan_adjacent_pixel(self, pixel, starting_colors):
        """Probe the two adjacent pixels if the first pixel returns a new color.

        Check the two pixels beside the pixel that was just checked to see
        if the edge is increasing or decreasing on an angle that is less than
        45 degrees.

        Args:
            pixel (Pixel): The original pixel.
            starting_colors (List[str]): The original colors to check against.

        Returns:
            Pixel: The pixel to move to.
        """
        starting_coords = pixel.coords
        adjacent_directions = Direction.get_adjacent_direction(self.direction)

        for adjacent_direction in adjacent_directions:
            pixel.move(adjacent_direction, steps=1)

            if pixel.colors_intersect(starting_colors):
                return pixel

            # Reset the pixel to the original.
            pixel.update_coords(*starting_coords)

        return pixel

    def walk(self, starting_coords, steps=1):
        """Walk a stright line of pixels until a new color is reached.

        Begining at the starting coordinates continue incrementally
        in the given direction until a new color is reached. At each new
        pixel arrived at check the pixels color. Given that the color name
        detection can be unreliable we need to get the three most likely colors
        and compare against the three most likely starting colors. If there are
        no common elements for two iterations we consider an edge to be found
        and exit. This provides us with minimal error recovery.

        Args:
            starting_coords (Pixel): Coordinates of the starting pixel.
            steps (int): The amount of pixels to skew on each interation.

        Returns:
            Pixel: The coordinates of a pixel.
        """
        starting_coords = starting_coords.coords
        pixel = Pixel(self.image, starting_coords)
        starting_colors = pixel.colors

        while pixel.colors_intersect(
                starting_colors) and not pixel.out_of_bounds():
            pixel.move(self.direction, steps)

            if self.depth == 'outer':
                if not pixel.colors_intersect(starting_colors):
                    pixel = self.scan_adjacent_pixel(pixel, starting_colors)

        return pixel

    def scan(self, starting_pixel):
        """Probe the direction until part of the ring is found.

        In some cases we may not have a fully formed ring, so in order to
        determine where the ring begins we need to check along a line of pixels
        and if not part of the ring is found, we skew slightly and try again.
        Continue checking until an edge is found.

        TODO: We may need to have a limit to the number of rows checked.

        Args:
            starting_pixel (Pixel): The pixel to start from.

        Returns:
            Pixel: The coordinates of a pixel.
        """
        rows_checked = 0
        starting_coords = starting_pixel.coords
        pixel = self.walk(starting_pixel)

        while pixel.out_of_bounds():
            # Reset the pixel.
            pixel = Pixel(self.image, starting_coords)
            pixel.side_step(self.direction, rows_checked)
            pixel = self.walk(pixel)
            rows_checked += 1

        return pixel
