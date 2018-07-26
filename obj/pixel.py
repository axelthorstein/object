class Pixel:
    """A pixel in an image."""

    def __init__(self, image, coords, confidence='high'):
        self.image = image
        self.coords = coords
        self.confidence = confidence
        self.x = self.coords[0]
        self.y = self.coords[1]
        
    def get_color(self):
        """Get the pixel at the given coordinate.

        The confidence level determines the range of colors to search through.
        
        Args:
            coords (tuple of int): The coordinates of the pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        if self.confidence == 'high':
            return get_color(self.image.getpixel(self.coords))
        else:
            return get_most_likely_colors(self.image.getpixel(self.coords))
