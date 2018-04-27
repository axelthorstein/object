from enum import Enum
import cv2
from PIL import Image
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
        # TODO: fix
        # ring.center_coords = (90, 105)
        ring.center_coords = (ring.center_coords[1], ring.center_coords[0])

        cv2.circle(image, ring.center_coords,
            ring.inner_radius, (200, 20, 24), 1)
        cv2.circle(image, ring.center_coords,
            ring.outer_radius, (43, 0, 123), 1)
        cv2.circle(image, ring.center_coords, 2, (255, 33, 0), 1)
        cv2.imwrite(
            "/Users/axelthor/Projects/object/images/test_draw.png", image
            )
        
    def preprocess_image(self):
        """Crop, compress, and filter to image.

        The image needs to be saved and reopened so that it can be manipulated
        as an array, where as the processing happens on the image object.

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
        # elif self.strategy == "hough_transform":
        #     preprocessed_image = cv2.imread(self.image_path, 0)
        #     interpolated_image = cv2.medianBlur(preprocessed_image, 5)

        return interpolated_image, image_width

    def detect_circle(self):
        """Detect a circle in an image.

        Detect whether a ring exists in the photo within the center ~20% of
        the image, detected using a specified strategy.

        Returns:
            tuple of int: The colors of the ring.
        """
        # crop, compress, and blur image
        preprocessed_image, image_width = self.preprocess_image()
        
        center_pixel = int(image_width / 2)
        starting_center_coords = [center_pixel, center_pixel]

        # locate the ring colors using strategy
        ring = self.strategy(preprocessed_image,
            starting_center_coords, debug=self.debug)
        print(ring.overlay)


        # draw the ring onto a photo for visual validation
        if self.debug:
            self.draw_ring(preprocessed_image, ring)
        print("Valid ring found at: {}".format(ring))

        if ring.is_valid:
            print("ring is valid")
        else:
            DetectionException("No valid ring found: {}".format(ring))

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
