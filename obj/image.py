from os.path import dirname, abspath
from PIL import Image as pil_image
from PIL import ImageFilter

from obj.pixel import Pixel


class Image:
    """An interface for an image."""

    def __init__(self, image_path):
        self.image = self.preprocess_image(image_path)
        self.center_point = Pixel(
            self.image,
            (int(self.image.size[0] / 2), int(self.image.size[1] / 2)))

    def preprocess_image(self, image_path):  #pylint: disable=no-self-use
        """Crop, compress, and filter to image.

        The image needs to be saved and reopened so that it can be manipulated
        as an array, where as the processing happens on the image object.

        TODO: Preprocessing the image is super slow for some reason.

        Args:
            image_path (str): The path to the image.

        Returns:
            Image: The processed image.
        """
        image = pil_image.open(image_path)

        # self.filter()
        # self.compress()
        # self.crop()

        return image

    def draw_ring(self, ring):
        """Draw onto a new image the potentially found ring.

        Convert each edge and center coordinate black for a visual
        representation of the found ring.

        Args:
            ring (Ring): The ring.
        """
        pixel_matrix = self.image.load()
        debug_path = dirname(abspath(__file__)) + '/images/debug.png'

        for point in ring.color_sequence.points:
            pixel_matrix[point] = (0, 0, 0)

        self.image.save(debug_path)

    def compress(self):
        """Compress a photo.
        """
        self.image = self.image.thumbnail(
            (self.image.size[0], self.image.size[0]), pil_image.ANTIALIAS)

    def filter(self):
        """Filter a photo.
        """
        self.image = self.image.filter(ImageFilter.MedianFilter())

    def crop(self):
        """Crop the photo by creating to slightly larger than the ring overlay.
        """
        # TODO: Will need to adjust these values to match the actual overlay.
        self.image = self.image.crop(
            (self.center_point.x - (self.center_point.x * 0.6),
             self.center_point.y - (self.center_point.y * 0.3),
             self.center_point.x + (self.center_point.x * 0.6),
             self.center_point.y + (self.center_point.y * 0.3)))
