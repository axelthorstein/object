import warnings
from PIL import Image as pil_image

from object.pixel import Pixel
from image_filters.filters import rag_merge_filter
from image_filters.filters import median_filter
from image_filters.filters import sharpen


class Image:
    """An interface for an image."""

    def __init__(self,
                 image_path,
                 crop=True,
                 apply_filters=True,
                 merge_filter=False,
                 compress=True):
        self.crop = crop
        self.apply_filters = apply_filters
        self.merge_filter = merge_filter
        self.compress = compress
        self.image = self.preprocess_image(image_path)
        self.center_point = Pixel(
            self.image,
            (int(self.image.size[0] / 2), int(self.image.size[1] / 2)))

    def preprocess_image(self, image_path):  #pylint: disable=no-self-use
        """Crop, compress, and filter to image.

        The image needs to be saved and reopened so that it can be manipulated
        as an array, where as the processing happens on the image object.

        Todo:
            Find a way to being the image size as low as possible

        Args:
            image_path (str): The path to the image.

        Returns:
            Image: The processed image.
        """
        image = pil_image.open(image_path)

        if self.apply_filters:
            image = Image.filter(image, self.merge_filter)

        if self.crop:
            image = Image.crop(image)

        if self.compress:
            image.thumbnail((256, 256), pil_image.ANTIALIAS)

        return image

    def draw_ring(self, ring):
        """Draw onto a new image the potentially found ring.

        Convert each edge and center coordinate black for a visual
        representation of the found ring.

        Args:
            ring (Ring): The ring.
        """
        self.image.save('images/debug.png')
        pixel_matrix = self.image.load()
        debug_path = 'images/debug_ring.png'

        for point in ring.color_sequence.points:
            pixel_matrix[point] = (0, 0, 0)

        pixel_matrix[ring.center_point.coords] = (0, 0, 0)

        self.image.save(debug_path)

    @staticmethod
    def compress(image):
        """Compress the image so that it is a constant size.

        Args:
            image (Image): The image to compress.

        Returns:
            Image: A compressed image.
        """
        return image.thumbnail((256, 256), pil_image.ANTIALIAS)

    @staticmethod
    def filter(image, merge_filter):
        """Filter the image so that it consolidates colors.

        Notes:
            The merge filter is separate because it is considerably more
            computaionally intensive than the other filters, on the order of
            multiple seconds.

        Args:
            image (Image): The image.
            merge_filter (bool): Whether to apply the RAG merge filter.

        Returns:
            image (Image): The filtered image.
        """
        if merge_filter:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                image = rag_merge_filter(image)

        image = median_filter(image, blur_level=25)
        image = sharpen(image)

        return image

    @staticmethod
    def crop(image):
        """Crop the photo by creating to slightly larger than the ring overlay.

        Todo:
            Will need to adjust these values to match the actual overlay.

        Args:
            image (Image): The image to crop.

        Returns:
            Image: A cropped image.
        """
        center_point = (int(image.size[0] / 2), int(image.size[1] / 2))

        return image.crop((center_point[0] - (center_point[0] * 0.8),
                           center_point[1] - (center_point[1] * 0.8),
                           center_point[0] + (center_point[0] * 0.8),
                           center_point[1] + (center_point[1] * 0.8)))
