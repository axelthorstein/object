import os
import cv2
import matplotlib.image
from PIL import Image
import numpy as np

# from o.analyzer import Analyzer
from analyzer import Analyzer
import webcolors



class Ring2:
    """
    A ring object with a center point, and a distance radius to it's inner
    and outer rings.
    """

    def __init__(self, image, image_path, inner_circle, outer_circle):
        self.image = image
        self.image_path = image_path
        self.center_coords = (inner_circle[0], inner_circle[1])
        self.inner_radius = inner_circle[2]
        self.outer_radius = outer_circle[2]
        self.is_ring = (outer_circle[2] - inner_circle[2]) > 2
        self.colors = self.get_colors()

    def get_rgb(self, rgb):
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def get_secondary_color(self, image, primary_color):
        """
        The while will go out of bounds if the ring is too close to the top.
        """
        if self.is_ring:
            secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1]]))
        else:
            offset = self.outer_radius + 1
            secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1] + offset]))

            while secondary_color == primary_color:
                offset += 10
                secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1] + offset]))

        return secondary_color

    def get_rgb_coords(self):
        if self.is_ring:
            return (self.center_coords[0], ((self.outer_radius - self.inner_radius) // 2)
                    + self.inner_radius + self.center_coords[1])
        else:
            return (self.center_coords[0], self.inner_radius // 2 + self.center_coords[1])

    def get_colors(self):
        image = matplotlib.image.imread(self.image_path)

        rgb_coords = self.get_rgb_coords()

        primary_color = Analyzer.get_color(self.get_rgb(image[rgb_coords[0]][rgb_coords[1]]))
        secondary_color = self.get_secondary_color(image, primary_color)
        
        return (primary_color, secondary_color)

    def to_string(self):
        return "Detected a ring at the coordinates {} with a inner and \
outer radius of {} from {}.".format(
               self.center_coords, (self.inner_radius, self.outer_radius),
               os.path.basename(self.image_path).replace("_cropped.png", ""))


class Ring:
    """
    A ring based on the radii and edge points of two circles. This ring bounded by the same color inside and surrounding.

    Using a simple method of linearly analyzing pixels determine if a ring exists in an image. If a ring is found to be in the image, determine the two colors that the ring consists of.

    The description for this simple method can be found here:
    https://gist.github.com/axelthorstein/337312d5030af4b965e5a40271ba0361#simple
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.debug = debug
        self.left_inner_edge = self.walk(starting_coords, Ring.left)
        self.right_inner_edge = self.walk(starting_coords, Ring.right)
        self.up_inner_edge = self.walk(starting_coords, Ring.up)
        self.down_inner_edge = self.walk(starting_coords, Ring.down)
        self.center_coords = (self.get_center_x(), self.get_center_y())
        self.inner_radius = self.get_inner_radius()
        self.outer_radius = self.get_outer_radius()
        self.center_color = self.get_center_color()
        self.ring_color = self.get_ring_color()

    def get_center_color(self):
        """Find the color inside the circle.

        Returns:
            str: The center color.
        """
        return self.color(self.center_coords)

    def get_ring_color(self):
        """Find the color inside the ring.

        Returns:
            str: The ring color.
        """
        x = self.center_coords[0] + self.inner_radius + int((self.outer_radius - self.inner_radius) / 2)
        y = self.center_coords[1]

        return self.color((x, y))

    def get_inner_radius(self):
        """Find the radius of the inner circle.

        Returns:
            int: The inner radius.
        """
        return self.right_inner_edge[0] - self.center_coords[0]

    def get_outer_radius(self):
        """Find the radius of the outer circle.

        Returns:
            int: The outer radius.
        """
        return self.walk(Ring.right(self.right_inner_edge), Ring.right)[0] - self.center_coords[0]

    def get_center_x(self):
        """Find the center x coordinate of the ring based on the inner edges.

        Returns:
            int: The x coordinate of a pixel.
        """
        return int(self.left_inner_edge[0] + ((self.right_inner_edge[0] - self.left_inner_edge[0]) / 2))
        
    def get_center_y(self):
        """Find the center y coordinate of the ring based on the inner edges.

        Returns:
            int: The y coordinate of a pixel.
        """
        return int(self.down_inner_edge[1] + ((self.up_inner_edge[1] - self.down_inner_edge[1]) / 2))

    def up(coords):
        """Increment the y value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0], coords[1] + 1)

    def down(coords):
        """Decrement the y value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0], coords[1] - 1)

    def left(coords):
        """Decrement the x value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0] - 1, coords[1])

    def right(coords):
        """Increment the x value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0] + 1, coords[1])

    def get_colour_name(rgb):
        """Get the name of a color for a RGB value.

        Resolve the closest human readable name for a RBG value.

        Args:
            rgb (list of int): The Red, Green, Blue triplet.

        Returns:
            str: The color name from the RGB value.
        """
        min_colours = {}

        for key, name in webcolors.css21_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - rgb[0]) ** 2
            gd = (g_c - rgb[1]) ** 2
            bd = (b_c - rgb[2]) ** 2
            min_colours[(rd + gd + bd)] = name

        return min_colours[min(min_colours.keys())]

    def color(self, coords):
        """Return the name of a color for the given pixel.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return Ring.get_colour_name(tuple(self.image[coords[0], coords[1]]))

    def walk(self, starting_coords, direction):
        """Walk a stright line of pixels until a new color is reached.

        Begining at the given stating coordinates continue incrementally in the given direction until a new color is reached. At each new pixel arrived at check the pixels color.
        
        Args:
            starting_coords (tuple of int): The coordinates of the starting pixel.
            direction (method): The direction to increment/decrement.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        starting_color = self.color(starting_coords)
        next_coords = starting_coords
        next_color = self.color(direction(next_coords))

        while next_color == starting_color:
            next_coords = direction(next_coords)
            next_color = self.color(direction(next_coords))

        if self.debug:
            print("Walked {}, starting color: {} at {}, next color: {} at {}".format(direction.__name__, starting_color, starting_coords, next_color, next_coords))

        return next_coords

    def to_string(self):
        print("Ring: left {}, right {}, up {}, down {}, center {}, inner {}, outer {}, center color {}, ring_color {}".format(
                self.left_inner_edge, 
                self.right_inner_edge,
                self.up_inner_edge,
                self.down_inner_edge,
                self.center_coords,
                self.inner_radius,
                self.outer_radius,
                self.center_color,
                self.ring_color
            )
        )


class Detect:
    """
    Detect a circle from a given image.
    """

    def __init__(self, image_path, debug=True):
        self.image_path = image_path
        self.debug = debug

    def crop(self, image):
        """Crop a photo.

        Crop the photo by creating to slightly larger than the circle overlay.

        If debug is enabled save the newly cropped image to new path suffixed with "_cropped.png".

        Args:
            image (np.array of np.array): The path to the original image.

        Returns:
            np.array of np.array: The newly cropped image.
        """
        half_the_width = image.size[0] / 2
        half_the_height = image.size[1] / 2

        # TODO: Will need to adjust these values to match the actual overlay.
        cropped_image = image.crop(
            (
                half_the_width - (half_the_width * 0.25),
                half_the_height - (half_the_height * 0.35),
                half_the_width + (half_the_width * 0.25),
                half_the_height + (half_the_height * 0.35)
            )
        )

        if self.debug:
            cropped_path = self.image_path[:-4] + "_cropped.png"
            cropped_image.save(cropped_path)
        
        return cropped_image

    def compress(self, image):
        """Compress a photo.

        Args:
            image (np.array of np.array): The path to the original image.

        Returns:
            np.array of np.array: The newly cropped image.
        """
        image.thumbnail((image.size[0], image.size[0]), Image.ANTIALIAS)

        return image

    def draw_ring(self, image, ring):
        """Draw onto a new image the potentially found ring.

        Args:
            image (np.array of np.array): The original image.
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        cv2.circle(image, ring.center_coords, ring.inner_radius, (0, 255, 0), 1)
        cv2.circle(image, ring.center_coords, ring.outer_radius, (0, 255, 0), 1)
        cv2.circle(image, ring.center_coords, 2, (255, 0, 0), 1)
        cv2.imwrite("/Users/axelthor/Projects/object/images/test_draw.png", image)
        
    def preprocess_image(self):
        """Crop, compress, and filter to image.

        The image needs to be saved and reopened so that it can be manipulated as an array, where as the processing happens on the image object.

        Returns:
            np.array of np.array: The preprocessed image.
        """
        image = Image.open(self.image_path)

        preprocessed_image_path = self.image_path[:-4] + "_preprocessed.png"

        cropped_image = self.crop(image)
        compressed_image = self.compress(cropped_image)

        compressed_image.save(preprocessed_image_path)
        image_width = compressed_image.size[0]

        preprocessed_image = cv2.imread(preprocessed_image_path)

        interpolated_image = cv2.bilateralFilter(preprocessed_image, 9, 75, 75)

        return interpolated_image, image_width

    def detect_circle(self):
        """Detect whether a ring exists in the given photo.

        Returns:
            tuple of int: The colors of the ring.
        """
        # crop, compress, and blur image
        preprocessed_image, image_width = self.preprocess_image()
        
        # locate the ring colors
        center_pixel = int(image_width / 2)
        starting_center_coords = [center_pixel, center_pixel]
        ring = Ring(preprocessed_image, starting_center_coords, debug=self.debug)

        # draw the ring onto a photo for visual validation
        if self.debug:
            self.draw_ring(preprocessed_image, ring)

        return (ring.center_color, ring.ring_color)


class Detect_hard:
    """
    Detect a circle from a given image.
    """

    def __init__(self, image_path):
        self.image_path = self.compress(image_path)

    def compress(self, image_path):
        thumbnail_path = image_path[:-4] + "_cropped.png"
        image = Image.open(image_path)
        image.thumbnail((256, 256), Image.ANTIALIAS)
        image.save(thumbnail_path)
        
        return thumbnail_path

    def get_ring(self, image):

        def round(nums, precision=0):
            return np.uint16(np.around(nums, precision))

        # print(cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, .5, 20, 30, 30, 10, 10))

        c1 = round(cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, .5, 10, 10, 10, 10, 10)[0][0])
        c2 = round(cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.5, 10, 10, 10, 10, 10)[0][0])

        if c1[2] > c2[2]:
            outer_circle = c1
            inner_circle = c2
        else:
            outer_circle = c2
            inner_circle = c1

        if round(inner_circle[0:1], -1) == round(outer_circle[0:1], -1):
            return Ring(image, self.image_path, inner_circle, outer_circle)

    def draw_ring(self, ring, image): 
        gray_scale = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        if ring.outer_radius != ring.inner_radius:
            # Draw the outer circle
            cv2.circle(gray_scale, ring.center_coords, ring.outer_radius, (0, 255, 0), 2)
            # Draw the inner circle
            cv2.circle(gray_scale, ring.center_coords, ring.inner_radius, (255, 0, 0), 2)
        else:
            cv2.circle(gray_scale, ring.center_coords, ring.inner_radius, (255, 255, 0), 2)

        # Draw the center of the circle
        cv2.circle(gray_scale, ring.center_coords, 2, (0 , 0, 255), 3)

        cv2.imwrite(self.image_path, gray_scale)
        
    def detect_circle(self):
        image = cv2.imread(self.image_path, 0)
        image = cv2.medianBlur(image, 5)
        ring = self.get_ring(image)

        if ring:
            print(ring.to_string())
            self.draw_ring(ring, image)
            return ring.get_colors()
        else:
            print("No circles detected.")
        
        # os.remove(self.image_path)


if __name__=="__main__":
    Detect("/Users/axelthor/Projects/object/images/test2.png", debug=False).detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/thick_ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/two_rings.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/moon_ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/circle.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/moon.png').detect_circle()
