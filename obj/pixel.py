from utils.color_utils import get_color, get_most_likely_colors


class Pixel:
    """A pixel in an image."""

    def __init__(self, image, coords, color_range='css2', variance=2):
        self.image = image
        self.coords = coords
        self.color_range = color_range
        self.colors = self.get_color(coords)
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.variance = variance

    def get_color(self, coords):
        """Get the pixel at the given coordinate.

        The color range determines the range of colors to search through.

        Args:
            coords (tuple of int): The coordinates of the pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        if self.color_range == 'css2':
            return get_color(self.image.getpixel(coords))
        else:
            return get_most_likely_colors(self.image.getpixel(coords))

    def move(self, direction, steps):
        """

        """
        self.coords = direction(self.coords, steps=steps)
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.update_colors()

    def update_colors(self):
        """

        """
        if len(self.colors) > self.variance:
            new_colors = self.get_color(self.coords)
            self.colors = self.colors[len(new_colors):] + new_colors
        else:
            self.colors += self.get_color(self.coords)

    def colors_intersect(self, other_color):
        """Determine if last colors the pixel has seend, within the variance,
        does not contain the other color. 

        Example:
            row = ['w', 'w', 'w', 'g', 'w', 'w', 'g', 'g']


        """
        return other_color[0] in self.colors[-self.variance:]

    def out_of_bounds(self, steps=2):
        """

        """
        width, height = self.image.size

        return ((width - steps <= self.x) or (self.x <= steps) or
                (height - steps <= self.y) or (self.y <= steps))

    def __str__(self):
        desc = f'\n{self.__class__.__name__}:\n'

        for attribute in self.__dict__:
            desc += f'    {attribute.capitalize()} = {self.__dict__[attribute]},\n'

        return desc

    def __repr__(self):
        return self.__str__()
