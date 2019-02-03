from utils.color_utils import get_color, get_brightness, get_most_likely_colors


class Pixel:
    """A pixel in an image."""

    def __init__(self, image, coords):
        self.image = image
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.colors = self.get_color(coords)
        self.brightness_values = get_brightness(image.getpixel(coords))

    @property
    def color(self):
        """Return the last seen color.

        Returns:
            str: The color.
        """
        return self.colors[-1]

    @property
    def brightness(self):
        """Return the last seen brightness.

        Returns:
            str: The brightness.
        """
        return round(self.brightness_values[-1] * 100)

    def get_color(self, coords, color_range='css2'):
        """Get the pixel at the given coordinate.

        The color range determines the range of colors to search through.

        Args:
            coords (Tuple[int]): The coordinates of the pixel.
            color_range (str): The range of web colors to use.

        Returns:
            Tuple[int]: The coordinates of a pixel.

        Raises:
            PixelException: If the new coords are out of bounds.
        """
        if not self.out_of_bounds(coords):
            if color_range == 'css2':
                return get_color(self.image.getpixel(coords))

            return get_most_likely_colors(self.image.getpixel(coords))

        raise PixelException(f"The new coordinates {coords} are out of bounds.")

    def out_of_bounds(self, coords, steps=3):
        """Check if the new coordinates are at the edge of the image.

        Args:
            steps (int): The pixel margin to check.

        Returns:
            bool: Whether the new coordinates are at the edge of the image.
        """
        width, height = self.image.size

        return ((width - steps <= coords[0]) or (coords[0] < 0) or
                (height - steps <= coords[1]) or (coords[1] < 0))

    def __repr__(self):
        """Return a short, in line, description of the Pixel.

        Returns:
            str: The string representation of the Pixel.
        """
        return f'{self.__class__.__name__} at {self.coords} with {self.color} colors.'

    def __str__(self):
        """Return a full description of the Pixel.

        Returns:
            str: The string representation of the Pixel.
        """
        desc = f'\n{self.__class__.__name__}:\n'

        for attribute in self.__dict__:
            key = attribute.replace('_', ' ').capitalize()
            desc += f'    {key}: {self.__dict__[attribute]},\n'

        return desc


class PixelException(Exception):
    pass
