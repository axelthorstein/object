#pylint: skip-file

from enum import Enum
from profilehooks import timecall

from object.object import Object
from utils.logging_utils import logger
from object.image import Image
from object.overlay import Overlay

LOGGER = logger('object')


class DetectionStrategy(Enum):
    RING = Object


class Detector:
    """
    Detect a ring from a given image.
    """

    def __init__(self,
                 image_path,
                 strategy=DetectionStrategy.RING,
                 debug=False,
                 crop=True,
                 apply_filters=True,
                 merge_filter=False,
                 compress=True):
        self.image = Image(
            image_path,
            crop=crop,
            apply_filters=apply_filters,
            merge_filter=merge_filter,
            compress=compress)
        self.strategy = strategy.value
        self.debug = debug

    def log_debug_info(self, object):
        """Log debugging information.

        Log the overlay and object dimensions and draw them onto the image.

        Args:
            object (Object): The detected object.
        """
        self.image.draw_ring(object)

        if object.is_valid:
            LOGGER.debug("Valid object found at: {}".format(object))
        else:
            raise DetectionException("No valid object found: {}".format(object))

    @timecall
    def find_ring(self, grain=360):
        """Detect a ring in an image.

        Detect whether a ring exists in the photo within the center ~20% of
        the image, detected using a specified strategy.

        Todo:
            Try using crop hints to guess radius.
        
        Returns:
            tuple of int: The colors of the ring.
        """
        overlay = Overlay(self.image.center_point)

        ring = self.strategy(self.image.image, overlay.center_point,
                             overlay.radius * 1.35)

        ring.approximate(grain)

        if self.debug:
            self.log_debug_info(ring)

        return ring


class DetectionException(Exception):
    pass
