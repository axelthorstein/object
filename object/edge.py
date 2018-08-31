from object.pixel import Pixel


class Edge:
    """
    An interface for finding the next edge from a starting pixel.
    """

    def __init__(self, image, direction):
        self.image = image
        self.direction = direction

    def walk(self, starting_pixel, steps=1):
        """Walk a stright line of pixels until a new color is reached.

        Begining at the starting coordinates continue incrementally
        in the given direction until a new color is reached. At each new
        pixel arrived at check the pixels color. Given that the color name
        detection can be unreliable we need to get the three most likely colors
        and compare against the three most likely starting colors. If there are
        no common elements for two iterations we consider an edge to be found
        and exit. This provides us with minimal error recovery.

        Todo:
            Doing the adjacent pixel scanning on non outer edges may be making
            the detection slower.

        Args:
            starting_pixel (Pixel): Coordinates of the starting pixel.
            steps (int): The amount of pixels to skew on each interation.

        Returns:
            Pixel: The coordinates of a pixel.
        """
        starting_coords = starting_pixel.coords
        pixel = Pixel(self.image, starting_coords)
        starting_colors = pixel.colors

        while pixel.colors_intersect(
                starting_colors) and not pixel.out_of_bounds():
            pixel.move(self.direction, steps)

            if not pixel.colors_intersect(starting_colors):
                pixel.scan_adjacent_pixels(self.direction, starting_colors)

        return pixel

    def scan(self, starting_pixel):
        """Probe the direction until part of the ring is found.

        In some cases we may not have a fully formed ring, so in order to
        determine where the ring begins we need to check along a line of pixels
        and if not part of the ring is found, we skew slightly and try again.
        Continue checking until an edge is found.

        Todo:
            We may need to have a limit to the number of rows checked.

        Args:
            starting_pixel (Pixel): The pixel to start from.

        Returns:
            Pixel: The coordinates of a pixel.
        """
        rows_checked = 0
        starting_coords = starting_pixel.coords
        pixel = self.walk(starting_pixel)

        while pixel.out_of_bounds() and rows_checked < 100:
            # Reset the pixel.
            pixel = Pixel(self.image, starting_coords)
            pixel.side_step(self.direction, rows_checked)
            pixel = self.walk(pixel)
            rows_checked += 1

        return pixel
