from enum import Enum
from PIL import Image, ImageFilter
from profilehooks import timecall

from obj.hough_transform_ring import HoughTransform
from obj.dashed_ring import Dashed
from obj.logs import logger

LOGGER = logger('object')


class DetectionStrategy(Enum):
    HOUGH_TRANSFORM = HoughTransform
    DASHED = Dashed


class Detect:
    """
    Detect a ring from a given image.
    """

    def __init__(self,
                 image_path,
                 strategy=DetectionStrategy.DASHED,
                 debug=True):
        self.image_path = image_path
        self.strategy = strategy.value
        self.debug = debug

    def crop(self, image):
        """Crop a photo.

        Crop the photo by creating to slightly larger than the ring overlay.

        Args:
            image (Image): The path to the original image.

        Returns:
            Image: The newly cropped image.
        """
        half_the_width = image.size[0] / 2
        half_the_height = image.size[1] / 2

        # TODO: Will need to adjust these values to match the actual overlay.
        cropped_image = image.crop((half_the_width - (half_the_width * 0.5),
                                    half_the_height - (half_the_height * 0.5),
                                    half_the_width + (half_the_width * 0.5),
                                    half_the_height + (half_the_height * 0.5)))

        return cropped_image

    def compress(self, image):
        """Compress a photo.

        Args:
            image (Image): The path to the original image.

        Returns:
            Image: The newly cropped image.
        """
        image.thumbnail((image.size[0], image.size[0]), Image.ANTIALIAS)

        return image

    def draw_ring(self, image, ring):
        """Draw onto a new image the potentially found ring.

        Convert each edge and center coordinate black for a visual
        representation of the found ring.

        Args:
            image (Image): The original image.
            ring (Ring): The ring.
        """
        pixel_matrix = image.load()

        for point in ring.color_sequence.points:
            pixel_matrix[point] = (0, 0, 0)

        image.save("/Users/axelthor/Projects/object/images/test_draw.png")

    def preprocess_image(self):
        """Crop, compress, and filter to image.

        The image needs to be saved and reopened so that it can be manipulated
        as an array, where as the processing happens on the image object.

        TODO: Preprocessing the image is super slow for some reason.

        Returns:
            Image: The preprocessed image.
        """
        image = Image.open(self.image_path)
        # filtered_image = image.filter(ImageFilter.MedianFilter())

        # preprocessed_image = self.compress(self.crop(filtered_image))

        return image

    def log_debug_info(self, preprocessed_image, ring):
        """Log debugging information.

        Log the overlay and ring dimensions and draw them onto the image.

        Args:
            image (Image): The preprocessed image.
            ring (Ring): The detected ring.
        """
        self.draw_ring(preprocessed_image, ring)

        if ring.is_valid:
            LOGGER.info("Valid ring found at: {}".format(ring))
        else:
            raise DetectionException("No valid ring found: {}".format(ring))

    @timecall
    def detect_ring(self, grain=360):
        """Detect a ring in an image.

        Detect whether a ring exists in the photo within the center ~20% of
        the image, detected using a specified strategy.

        Returns:
            tuple of int: The colors of the ring.
        """
        # crop, compress, and blur image
        image = self.preprocess_image()

        # find the ring in the image
        starting_coords = (int(image.size[0] / 2), int(image.size[1] / 2))

        ring = self.strategy(image, starting_coords, debug=self.debug)

        ring.approximate(grain)

        if not ring.is_valid():
            ring.calculate(grain)

        if self.debug:
            self.log_debug_info(image, ring)

        return ring


class DetectionException(Exception):
    pass
