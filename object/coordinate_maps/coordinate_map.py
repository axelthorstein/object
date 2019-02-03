class CoordinateMap:
    """An abstract class for sampling the coordinates from a map."""

    def get_coordinates():
        """Abstract method for returning the coordinates of a map.

        Returns:
            List[Tuple[int, int]]: The sorted points on the circumference of the circle.
        """
        pass

    @staticmethod
    def deduplicate(elements):
        """Deduplicate a list of tuples.

        Args:
            elements (List[Tuple[int]]): The list of tuples.

        Returns:
            List[Tuple[int]]: The deduplicated list of tuples.

        Example:
            >>> deduplicate([(1, 2), (2, 3), (1, 2)])
            [(1, 2), (2, 3)]
            >>> deduplicate([(1, 2), (2, 3))
            [(1, 2), (2, 3)]
        """
        return list(set(elements))
