from profilehooks import timecall

from configs.config import PRODUCT_MAP
from utils.logging_utils import logger

LOGGER = logger('object')


class ProductException(Exception):
    pass


class Product:
    """A product."""

    def __init__(self, product_code):
        self.product_code = product_code
        self.product_name = self.get_name()

    def is_valid(self):
        """Determine whether the sequence is valid.

        Check every rotation of the coded sequence to see if it exists in the
        product map.

        Returns:
            str: The valid code or an empty string.
        """
        code = self.product_code

        if code in PRODUCT_MAP:
            return code

        for _ in code:
            code = code[1:] + code[0]

            if code in PRODUCT_MAP:
                return code

        return ''

    # def check_similar(code):
    #     """
    #     """
    # from difflib import SequenceMatcher

    #     most_likely = (0, None)

    #     for _ in code:
    #         code = code[1:] + code[0]

    #         for product in PRODUCT_MAP:
    #             if similarity >= most_likely[0]:
    #                 most_likely = (similarity, product)
    #             similarity = SequenceMatcher(None, code, product).ratio()

    #     if most_likely[0] > 0.8:
    #         return most_likely[1]

    @timecall
    def get_name(self):
        """Return the product based on the ring in the image.

        Returns:
            str: The product ID.
        """
        valid_product_code = self.is_valid()

        if valid_product_code:
            return PRODUCT_MAP[valid_product_code]

        return ''
