from difflib import SequenceMatcher
from profilehooks import timecall

from configs.config import PRODUCT_MAP
from utils.logging_utils import logger

LOGGER = logger('object')


class ProductException(Exception):
    pass


class Product:
    """A product."""

    def __init__(self, sequence):
        self.color_code = sequence.color_code
        self.brightness_values = sequence.brightness_values
        self.product_name = self.get_name()

    @staticmethod
    def is_valid(code):
        """Determine whether the sequence is valid.

        Check every rotation of the coded sequence to see if it exists in the
        product map.

        Returns:
            str: The valid code or an empty string.
        """
        # Constant time check.
        if code in PRODUCT_MAP:
            return code

        # O(n) time check.
        for _ in code:
            code = code[1:] + code[0]
            if code in PRODUCT_MAP:
                return code

        # O(n^2+) time check.
        similar, _ = Product.check_similar(code, PRODUCT_MAP)
        if similar:
            return similar

        return ''

    @staticmethod
    def check_similar(code, products):
        """Return a product code if it is within a threshhold of similarity.

        Todo:
            - This function is a huge speed bottleneck. Ideally I would like to
            be able to register sequences that are similar but not exact
            matches, but I want to find a faster way of doing it.

        Args:
            code (str): The detected sequence from an image.
            products (dict): The map of product sequences to names.

        Returns:
            str, float: The similar code and the similarity.
        """
        similar_code = None
        max_similarity = 0
        similarity_threshold = 0.9

        for _ in code:
            code = code[1:] + code[0]

            for product in products:
                if code == product:
                    return product, 1

                similarity = SequenceMatcher(None, code, product).ratio()
                if similarity == 1:
                    return product, similarity

                if similarity >= max_similarity:
                    similar_code = product
                    max_similarity = round(similarity, 2)

        if max_similarity >= similarity_threshold:
            return similar_code, max_similarity

        return None, max_similarity

    @timecall
    def get_name(self):
        """Return the product based on the ring in the image.

        Returns:
            str: The product ID.
        """
        valid_product_code = (Product.is_valid(self.color_code) or
                              Product.is_valid(self.brightness_values))

        if valid_product_code:
            return PRODUCT_MAP[valid_product_code]

        return None
