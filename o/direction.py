class DirectionException(Exception):
    pass
        
class Direction:
    """
    An interface for incrementing coordinates in a pixel matrix.
    """

    @staticmethod
    def get_directions():
        """Return a mapping of directions to methods.
        
        Return:
            dictionary: The directions mapping.
        """
        directions = {
            "left": Direction.left,
            "up": Direction.up,
            "right": Direction.right,
            "down": Direction.down
        }

        return directions

    @staticmethod
    def valid_coordinate(coord):
        """Return the coordinate if it is valid.
        
        Args:
            coord (int): The coordinate.

        Return:
            int: The valid coordinate.
        """
        if coord >= 0:
            return coord
        raise DirectionException(
            "A coordinate cannot be less than zero. {}".format(coord))

    @staticmethod
    def left(coords, jump=1):
        """Decrement the x value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        new_coordinate = Direction.valid_coordinate(coords[0] - jump)

        return (new_coordinate, coords[1])

    @staticmethod
    def up(coords, jump=1):
        """Increment the y value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0], coords[1] + jump)

    @staticmethod
    def down(coords, jump=1):
        """Decrement the y value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        new_coordinate = Direction.valid_coordinate(coords[1] - jump)

        return (coords[0], coords[1] - jump)

    @staticmethod
    def right(coords, jump=1):
        """Increment the x value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0] + jump, coords[1])
