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
            "left_and_up": Direction.left_and_up,
            "up": Direction.up,
            "right_and_up": Direction.right_and_up,
            "right": Direction.right,
            "right_and_down": Direction.right_and_down,
            "down": Direction.down,
            "left_and_down": Direction.left_and_down,
        }

        return directions

    @staticmethod
    def get_adjacent_direction(direction):
        """Return the directions that are adjacent to the original direction.
        
        Return:
            tuple of Directions: The adjacent directions.
        """
        if direction in (Direction.left, Direction.right):
            return (Direction.up, Direction.down)
        elif direction in (Direction.up, Direction.down):
            return (Direction.left, Direction.right)
        elif direction == Direction.left_and_down:
            return (Direction.left, Direction.down)
        elif direction == Direction.left_and_up:
            return (Direction.left, Direction.up)
        elif direction == Direction.right_and_up:
            return (Direction.right, Direction.up)
        elif direction == Direction.right_and_down:
            return (Direction.right, Direction.down)
        else:
            raise DirectionException(f"Direction {direction.__name__} not found.")

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
        raise DirectionException(f"A coordinate cannot be less than zero. {coord}")

    @staticmethod
    def left(coords, steps=1):
        """Decrement the x value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        new_coordinate = Direction.valid_coordinate(coords[0] - steps)

        return (new_coordinate, coords[1])

    @staticmethod
    def up(coords, steps=1):
        """Increment the y value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0], coords[1] - steps)

    @staticmethod
    def down(coords, steps=1):
        """Decrement the y value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        new_coordinate = Direction.valid_coordinate(coords[1] - steps)

        return (coords[0], coords[1] + steps)

    @staticmethod
    def right(coords, steps=1):
        """Increment the x value by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0] + steps, coords[1])

    @staticmethod
    def left_and_up(coords, steps=1):
        """Increment the x and y values by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        new_coordinate = Direction.valid_coordinate(coords[0] - steps)

        return (new_coordinate, coords[1] - steps)

    @staticmethod
    def right_and_up(coords, steps=1):
        """Increment the x and y values by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        return (coords[0] + steps, coords[1] - steps)

    @staticmethod
    def right_and_down(coords, steps=1):
        """Increment the x and y values by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        new_coordinate = Direction.valid_coordinate(coords[1] + steps)

        return (coords[0] + steps, new_coordinate)

    @staticmethod
    def left_and_down(coords, steps=1):
        """Increment the x and y values by 1.

        Args:
            coords (tuple of int): The coordinates of a pixel.

        Returns:
            tuple of int: The coordinates of a pixel.
        """
        new_coordinate = Direction.valid_coordinate(coords[1] + steps)

        return (coords[0] - steps, new_coordinate)
