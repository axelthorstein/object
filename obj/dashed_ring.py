from collections import Counter
from profilehooks import timecall
from PIL import Image, ImageFont, ImageDraw
import math
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
        inner_coordinate = Coordinate(self.image, 'inner')
        outer_coordinate = Coordinate(self.image, 'outer')
        directions = Direction.get_directions()
        black_pixel = (0, 0, 0)
        pixel_matrix = self.image.load()
        ring_distances = []
        center_distances = []
        draw = ImageDraw.Draw(self.image)

        for direction in directions:
            inner_pixel = inner_coordinate.probe(self.center_coords,
                                                 directions[direction])
            print(direction, inner_pixel.colors[-1])
            outer_pixel = outer_coordinate.probe(inner_pixel.coords,
                                                 directions[direction])
            print(direction, outer_pixel.colors[-1])
            pixel_matrix[inner_pixel.coords] = black_pixel
            pixel_matrix[outer_pixel.coords] = black_pixel
            center_distance = math.hypot(self.center_coords[0] - inner_pixel.x, self.center_coords[1] - inner_pixel.y)
            ring_distance = math.hypot(inner_pixel.x - outer_pixel.x, inner_pixel.y - outer_pixel.y)
            center_distances.append(center_distance)
            ring_distances.append(ring_distance)

        average_center_distance = sum(center_distances) / len(center_distances)
        average_ring_distance = sum(ring_distances) / len(ring_distances)
        radius = int(average_center_distance + (average_ring_distance / 2))
        print(f"center: {average_ring_distance}, ring: {average_center_distance}, middle_ring_distance: {radius}")
        pixel_matrix[self.center_coords] = black_pixel

        draw.ellipse((0,0,10,10), fill="black", outline = "blue")
        x, y =  self.image.size
        draw.ellipse((x/2-radius, y/2-radius, x/2+radius, y/2+radius), outline="black")

        self.image.save("/Users/axelthor/Projects/object/images/test_draw.png")

        exit()
