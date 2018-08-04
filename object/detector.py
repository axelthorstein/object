#pylint: skip-file

from enum import Enum
from profilehooks import timecall

from object.ring import Ring
from object.logs import logger
from object.image import Image

LOGGER = logger('object')


class DetectionStrategy(Enum):
    RING = Ring


class Detector:
    """
    Detect a ring from a given image.
    """

    def __init__(self, image_path, strategy=DetectionStrategy.RING, debug=True):
        self.image = Image(image_path)
        self.strategy = strategy.value
        self.debug = debug

    def log_debug_info(self, ring):
        """Log debugging information.

        Log the overlay and ring dimensions and draw them onto the image.

        Args:
            ring (Ring): The detected ring.
        """
        self.image.draw_ring(ring)

        if ring.is_valid:
            LOGGER.info("Valid ring found at: {}".format(ring))
        else:
            raise DetectionException("No valid ring found: {}".format(ring))

    @timecall
    def detect(self, grain=360):
        """Detect a ring in an image.

        Detect whether a ring exists in the photo within the center ~20% of
        the image, detected using a specified strategy.

        Returns:
            tuple of int: The colors of the ring.
        """
        # crop, compress, and blur image

        # find the ring in the image

        ring = self.strategy(
            self.image.image, self.image.center_point, debug=self.debug)

        ring.approximate(grain)

        if not ring.is_valid():
            ring.calculate(grain)

        if self.debug:
            self.log_debug_info(ring)

        return ring


class DetectionException(Exception):
    pass
