from obj.direction import Direction
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
        self.distance_moved = 0

    def get_color(self, coords):
        """Get the pixel at the given coordinate.

        The color range determines the range of colors to search through.

        Args:
            coords (Tuple[int]): The coordinates of the pixel.

        Returns:
            Tuple[int]: The coordinates of a pixel.
        """
        if self.color_range == 'css2':
            return get_color(self.image.getpixel(coords))

        return get_most_likely_colors(self.image.getpixel(coords))

    def side_step(self, direction, steps):
        """Move to a perpendicular row to the one that was just checked.

        Alternate the direction to move to based on the number of rows that
        have been checked so far.

        TODO: Change the function name to something more explicit.

        Args:
            steps (int): The number of rows checked.
            direction (method): Direction to increment/decrement.
        """
        if direction in [Direction.left, Direction.right]:
            if steps % 2 == 0:
                direction = Direction.up
            else:
                direction = Direction.down
        elif steps % 2 == 0:
            direction = Direction.left
        else:
            direction = Direction.right

        self.move(direction, steps=steps)

    def move(self, direction, steps):
        """Increment the pixels location and update relevant attributes.

        Args:
            direction (Direction): The direction to increment/decrement.
            steps (int): The amount of pixel spaces to move.
        """
        self.coords = direction(self.coords, steps=steps)
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.update_colors()
        # TODO: Try to use this instead of actually calculating the radius.
        self.distance_moved += 1

    def update_colors(self):
        """Update the most recent colors the pixel has seen.
        """
        if len(self.colors) > self.variance:
            new_colors = self.get_color(self.coords)
            self.colors = self.colors[len(new_colors):] + new_colors
        else:
            self.colors += self.get_color(self.coords)

    def update_coords(self, x, y):
        """Update the pixels coordinates to specified values.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.
        """
        self.coords = (x, y)
        self.x = x
        self.y = y

    def colors_intersect(self, other_color):
        """Determine if last colors the pixel has seen.

        Check within the variance that the pixel does not contain the other
        color.

        Args:
            other_color (list of str): The color to compare against.

        Returns:
            bool: Whether if we've entered a new color space.
        """
        return other_color[0] in self.colors[-self.variance:]

    def out_of_bounds(self, steps=2):
        """Check if the pixel is at the edge of the image.

        Args:
            steps (int): The pixel margin to check.

        Returns:
            bool: Whether the pixel is at the edge of the image..
        """
        width, height = self.image.size

        return ((width - steps <= self.x) or (self.x <= steps) or
                (height - steps <= self.y) or (self.y <= steps))

    def __repr__(self):
        """Return a short, in line, description of the Pixel.

        Returns:
            str: The string representation of the Pixel.
        """
        return f'Pixel {self.coords} with {self.colors} colors.'

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
