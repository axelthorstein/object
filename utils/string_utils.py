def are_rotations(string1, string2):
    """Check if strings are rotations of each other.

    You can tell if a string is a rotated version of another string if it's
    inside a duplicated version of the first string.

    TODO: Added tests.

    Examples:
        >>> s1 = "abcd"
        >>> s2 = "cdab"
        >>> "cdab" in "abcdabcd"
        True

    Args:
        string1 (str): First string to check against.
        string2 (str): Second string to check against.

    Returns:
        bool: If the strings are rotations of each other
    """
    if len(string1) == len(string2) and string2 in string1 + string1:
        return True

    return False
