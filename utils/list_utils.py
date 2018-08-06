from itertools import groupby
from collections import Counter


def left_strip(elements, element_to_strip):
    """Remove preceeding center color occurences.

    Slice the list from the first non center color occurance to the
    end of the list.

    Args:
        elements (List[str]): The unstriped list of elements.
        element_to_strip (str): The element to strip from the list.

    Returns:
        List[str]: The list left striped of the element.

    Example:
        >>> left_strip(['1', '2', '2', '3'], '1')
        ['2', '2', '3']
        >>> left_strip(['1', '2', '2', '3'], '2')
        ['1', 2', '2', '3']
    """
    if elements and elements[0] == element_to_strip:
        for elem in elements:
            if elem != element_to_strip:
                return elements[elements.index(elem):]

    return elements


def most_common_element(elements):
    """Return the most common element for a list.

    If there are two or more that have the same amount of occurences, then take
    the first occuring element. If the list is empty, just return the list.

    Args:
        elements (List[str]): The list of elements.

    Returns:
        str: The most common element.

    Example:
        >>> most_common_element(['1', '2', '2', '3'])
        ['2']
        >>> most_common_element([])
        []
    """
    most_common = Counter(elements).most_common(1)

    if most_common:
        return [most_common[0][0]]

    return most_common


def groupby_with_delimiter(elements, delimiter):
    """Groupby the elements separated by the delimiter.

    Group each slice of elements that are segmented by the delimiter. For each
    group of elements, including the delimiter groups, group them by the most
    common element.

    Todo:
        Find the max value over the group of delimiters.

    Args:
        elements (List[str]): The list of elements.
        delimiter (str): The element to separate groups.

    Returns:
        str: The list of grouped elements.

    Example:
        >>> groupby_with_delimiter(['1', '2', '2', '1', '4', '1'], '1')
        ['2', '4']
        >>> groupby_with_delimiter(['1', '2', '2', '3', '1', '4'], '1')
        ['2', '4']
    """
    grouped_list = []
    start_index = 0

    for end_index, elemment in enumerate(elements):
        if elemment == delimiter or end_index == len(elements) - 1:
            segment = list(
                filter(lambda x: x != delimiter,
                       elements[start_index:end_index + 1]))
            elemment = most_common_element(segment)
            grouped_list += elemment
            start_index = end_index

    return grouped_list


def group_by(elements):
    """Group the elements by elements that are beside identical elements.

    Args:
        elements (List[str]): The list of elements.

    Returns:
        List[str]: The list of grouped elements.

    Example:
        >>> group_by(['1', '1', '2', '3', '4', '1'])
        ['1', '2', '3', '4', '1']
    """
    grouped_list = []

    for group in groupby(elements, lambda x: x):
        grouped_list.append(group[0])

    return grouped_list


def shift_slice(unshifted_list, element_to_shift_on):
    """Shift a slice of elements from the front of the list to the back.

    Shift the slice of elements before the first occurence of element to shift
    on to the back of the list.

    Note:
        This function assumes that the element to shift on has been stripped
        from the front of the list.

    Args:
        unshifted_list (List[str]): The list of elements.
        element_to_shift_on (str): The element to shift on.

    Returns:
        List[str]: The shifted list.

    Example:
        >>> shift_slice(['1', '1', '2', '3', '4', '1'], element_to_shift_on='1')
        ['1', '1', '2', '3', '4', '1']
        >>> shift_slice(['2', '3', '4', '1', '1', '1'], element_to_shift_on='1')
        ['1', '1', '1', '2', '3', '4']
    """
    if unshifted_list and unshifted_list[0] != element_to_shift_on:
        first_element = unshifted_list.index(element_to_shift_on)

        return unshifted_list[first_element:] + unshifted_list[:first_element]

    return unshifted_list


def collapse(colors, center_color):
    """Collapse the colors into a sequence.

    The numbers of colors in the list will be determined by how many points
    were sampled from the image so we need to collapse them into one color
    per distinct change in color. A distinct change in color is indicated by
    changing from the delimiting color (center color) to a new color and
    back to the delimiting color. The max of each of these groups is taken
    in cause there is a small margin of error in the color identification.
    The end result being a list of one color per dash in the sequence and
    all of the delimiting colors removed.

    Args:
        List[str]: The sequence of colors from the image.

    Returns:
        List[str]: The collapsed sequence of colors.
    """

    sequence = []

    if len(set(colors)) >= 1:
        # If the ring is solid there will be no center colors present so k
        if center_color not in colors:
            return group_by(colors)

        # Group colors so that the center color is first.
        colors = shift_slice(colors, center_color)

        # Strip leftmost occurences of the center color.
        colors = left_strip(colors, center_color)

        # Group the elements by the most common per segment.
        sequence = groupby_with_delimiter(colors, center_color)

    return sequence
