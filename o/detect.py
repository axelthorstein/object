from enum import Enum
import cv2
from PIL import Image, ImageFilter
import numpy as np

from ring import SimpleRing, HoughTransformRing


class DetectionStrategy(Enum):
    SIMPLE = SimpleRing
    HOUGH_TRANSFORM = HoughTransformRing


class Detect:
    """
    Detect a circle from a given image.
    """

    def __init__(self, image_path,
                 strategy=DetectionStrategy.SIMPLE, debug=True):
        self.image_path = image_path
        self.strategy = strategy.value
        self.debug = debug

    def crop(self, image):
        """Crop a photo.

        Crop the photo by creating to slightly larger than the circle overlay.

        If debug is enabled save the newly cropped image to new path suffixed
        with "_cropped.png".

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

        # if self.debug:
        #     cropped_path = self.image_path[:-4] + "_cropped.png"
        #     cropped_image.save(cropped_path)
        
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

        Convert each edge and center coordinate black for a visual
        representation of the found ring.

        Args:
            image (Image): The original image.
            coords (tuple of int): The coordinates of a pixel.
        """
        pixel_matrix = image.load()
        black_pixel = (0,0,0)

        for coord in ring.inner_edges:
            pixel_matrix[ring.inner_edges[coord]] = black_pixel

        for coord in ring.outer_edges:
            pixel_matrix[ring.outer_edges[coord]] = black_pixel

        pixel_matrix[ring.center_coords] = (0, 250, 0)

        image.save("/Users/axelthor/Projects/object/images/test_draw.png")

    def preprocess_image(self):
        """Crop, compress, and filter to image.

        The image needs to be saved and reopened so that it can be manipulated
        as an array, where as the processing happens on the image object.

        Returns:
            Image: The preprocessed image.
        """
        image = Image.open(self.image_path)
        filtered_image = image.filter(ImageFilter.MedianFilter())

        preprocessed_image = self.compress(self.crop(filtered_image))

        return preprocessed_image

    def log_debug_info(self, preprocessed_image, ring):
        """Log debugging information.

        Log the overlay and ring dimensions and draw them onto the image.
        """
        self.draw_ring(preprocessed_image, ring)

        print(ring.overlay)

        if ring.is_valid:
            print("Valid ring found at: {}".format(ring))
        else:
            raise DetectionException("No valid ring found: {}".format(ring))

    def detect_circle(self):
        """Detect a circle in an image.

        Detect whether a ring exists in the photo within the center ~20% of
        the image, detected using a specified strategy.

        Returns:
            tuple of int: The colors of the ring.
        """
        # crop, compress, and blur image
        image = self.preprocess_image()
        
        starting_coords = (int(image.size[0] / 2), int(image.size[1] / 2))

        ring = self.strategy(image, starting_coords, debug=self.debug)

        # draw the ring onto a photo for visual validation
        if self.debug:
            self.log_debug_info(image, ring)

        return (ring.center_color, ring.ring_color)


class DetectionException(Exception):
    pass


if __name__=="__main__":
    Detect("/Users/axelthor/Projects/object/images/test3.png", strategy=DetectionStrategy.SIMPLE, debug=True).detect_circle()
    # Detect("/Users/axelthor/Projects/object/images/test3.png", strategy=HOUGH_TRANSFORM, debug=False).detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/thick_ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/two_rings.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/moon_ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/circle.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/moon.png').detect_circle()
