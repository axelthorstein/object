from collections import Counter
from profilehooks import timecall

from obj.ring import Ring
from obj.coordinate import Coordinate
from obj.direction import Direction
from obj.overlay import Overlay


class Dashed(Ring):
    """
    A ring based on the radii and edge points of two circles. This ring
    bounded by the same color inside and surrounding.

    Using a simple method of linearly analyzing pixels determine if a
    ring exists in an image. If a ring is found to be in the image,
    determine the two colors that the ring consists of.

    The description for this simple method can be found here:
    https://gist.github.com/axelthorstein/337312d5030af4b965e5a40271ba0361
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.debug = debug
        self.center_coords = starting_coords

    def create(self):
        """Set all of the dynamic attributes of the Ring.
        """
        coordinate = Coordinate(self.image, 'inner')
        print(self.center_coords)
        print(coordinate.get_pixel_colors((65, 276)))
        print(coordinate.get_pixel_colors((255, 276)))
