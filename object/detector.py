#pylint: skip-file

from profilehooks import timecall

from object.coordinate_maps.dashed_ring_map import DashedRingMap
from object.sequence import Sequence
from utils.logging_utils import logger

LOGGER = logger('object')


class Detector:
    """
    Detect an object from a given image.
    """

    def __init__(self, image, coordinate_map=DashedRingMap, debug=False):
        self.image = image
        self.coordinate_map = coordinate_map
        self.debug = debug

    @timecall
    def get_sequence(self):
        """Detect an object in an image.

        Todo:
            Try using crop hints to guess radius.

        Returns:
            OBject: The detected object.
        """
        coordinates = self.coordinate_map(self.image.center_point).coordinates

        # Apply coodinate map to image and get value sequence
        sequence = Sequence(self.image, self.image.center_point, coordinates)

        if self.debug:
            self.image.draw_ring(coordinates)
        return sequence


class DetectionException(Exception):
    pass
