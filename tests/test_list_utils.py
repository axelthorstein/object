from utils.list_utils import left_strip
from utils.list_utils import most_common_element
from utils.list_utils import groupby_with_delimiter
from utils.list_utils import group_by
from utils.list_utils import shift_slice
from utils.list_utils import collapse


def test_list_utils_left_strip_single_element():
    """
    Test that the single element to strip is stripped from the left of the list.
    """
    elements = ['1', '2', '1']
    element_to_strip = '1'
    expected = ['2', '1']
    actual = left_strip(elements, element_to_strip)

    assert expected == actual


def test_list_utils_left_strip_multiple_element():
    """
    Test that the multiple elements to strip are stripped from the left of the
    list.
    """
    elements = ['1', '1', '1', '2', '2', '1']
    element_to_strip = '1'
    expected = ['2', '2', '1']
    actual = left_strip(elements, element_to_strip)

    assert expected == actual


def test_list_utils_left_strip_strip_no_elements():
    """
    Test that the no elements to strip are stripped from the left of the list.
    """
    elements = ['2', '2', '1']
    element_to_strip = '1'
    expected = ['2', '2', '1']
    actual = left_strip(elements, element_to_strip)

    assert expected == actual


def test_list_utils_left_strip_no_elements():
    """
    Test that the no elements in the list returns back the list.
    """
    elements = []
    element_to_strip = '1'
    expected = []
    actual = left_strip(elements, element_to_strip)

    assert expected == actual


def test_list_utils_most_common_element():
    """
    Test that the most common element in the list is returned.
    """
    elements = ['2', '2', '1']
    expected = ['2']
    actual = most_common_element(elements)

    assert expected == actual


def test_list_utils_most_common_element_return_first():
    """
    Test that the first most common element in the list is returned.
    """
    elements = ['2', '2', '1', '1']
    expected = ['2']
    actual = most_common_element(elements)

    assert expected == actual


def test_list_utils_most_common_element_no_elements():
    """
    Test that the list is returned back.
    """
    elements = []
    expected = []
    actual = most_common_element(elements)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_no_elements():
    """
    Test that the empty list is returned back.
    """
    elements = []
    delimiter = '1'
    expected = []
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_single_element():
    """
    Test that the an empty list is returned back.
    """
    elements = ['1']
    delimiter = '1'
    expected = []
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_multiple_elements():
    """
    Test that the list is returned back with the elements grouped.
    """
    elements = ['1', '2', '2', '1', '4', '1']
    delimiter = '1'
    expected = ['2', '4']
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_multiple_elements_max_value():
    """
    Test that the list is returned back with the elements grouped, with each
    group returning the value that occurs most often.
    """
    elements = ['1', '2', '2', '3', '1', '4']
    delimiter = '1'
    expected = ['2', '4']
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_delimiter_doesnt_start():
    """
    Test that the list is returned back with the elements grouped, with each
    group returning the value that occurs most often when the delimiter doesn't
    start the list.
    """
    elements = ['2', '2', '3', '1', '4']
    delimiter = '1'
    expected = ['2', '4']
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_no_delimiters():
    """
    Test that the list is only the most common element because the delimiter is
    not present.
    """
    elements = ['2', '2', '3', '4']
    delimiter = '1'
    expected = ['2']
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_delimiters_removed():
    """
    Test that the delimiter is removed from the list.
    """
    elements = ['2', '2', '1', '1', '1', '1', '1', '3', '4']
    delimiter = '1'
    expected = ['2', '3']
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_large_list():
    """
    Test that the list is only the most common element because the delimiter is
    not present.
    """
    elements = ['1', '1', '2', '2', '3', '1', '4', '1', '4', '3', '1', '1', '1']
    delimiter = '1'
    expected = ['2', '4', '4']
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_with_delimiter_two_elements():
    """
    Test that only the non delimiter is returned.
    """
    elements = ['2', '1']
    delimiter = '1'
    expected = ['2']
    actual = groupby_with_delimiter(elements, delimiter)

    assert expected == actual


def test_list_utils_groupby_no_elements():
    """
    Test that an empty list is returned.
    """
    elements = []
    expected = []
    actual = group_by(elements)

    assert expected == actual


def test_list_utils_groupby_single_elements():
    """
    Test that a list with the single element is returned.
    """
    elements = ['1']
    expected = ['1']
    actual = group_by(elements)

    assert expected == actual


def test_list_utils_groupby_multiple_elements():
    """
    Test that a list with the multiple elements grouped is returned.
    """
    elements = ['1', '1', '2', '2', '1', '3', '3', '3', '3', '1']
    expected = ['1', '2', '1', '3', '1']
    actual = group_by(elements)

    assert expected == actual


def test_list_utils_shift_slice_no_elements():
    """
    Test that an empty list is returned.
    """
    unshifted_list = []
    elem_to_shift_on = '1'
    expected = []
    actual = shift_slice(unshifted_list, elem_to_shift_on)

    assert expected == actual


def test_list_utils_shift_slice_single_elements():
    """
    Test that an empty list is returned.
    """
    unshifted_list = ['1']
    elem_to_shift_on = '1'
    expected = ['1']
    actual = shift_slice(unshifted_list, elem_to_shift_on)

    assert expected == actual


def test_list_utils_shift_slice_two_elements_no_shift():
    """
    Test that the list is returned as is.
    """
    unshifted_list = ['1', '2']
    elem_to_shift_on = '1'
    expected = ['1', '2']
    actual = shift_slice(unshifted_list, elem_to_shift_on)

    assert expected == actual


def test_list_utils_shift_slice_two_elements_shifts():
    """
    Test that the list is returned reversed.
    """
    unshifted_list = ['2', '1']
    elem_to_shift_on = '1'
    expected = ['1', '2']
    actual = shift_slice(unshifted_list, elem_to_shift_on)

    assert expected == actual


def test_list_utils_shift_slice_multiple_elements():
    """
    Test that all the elements before the element to shift on are moved to the
    end of the list.
    """
    unshifted_list = ['2', '3', '4', '1', '1', '1']
    elem_to_shift_on = '1'
    expected = ['1', '1', '1', '2', '3', '4']
    actual = shift_slice(unshifted_list, elem_to_shift_on)

    assert expected == actual


def test_list_utils_collapse(center_element):
    """
    Test that the elements are collapsed so that the max of each group of elements
    is surfaced.
    """
    elements = ['1', '2', '1']
    expected = ['2']
    actual = collapse(elements, center_element)

    assert expected == actual


def test_list_utils_collapse_single_element(center_element):
    """
    Test that the elements are collapsed so that the max of each group of elements
    is surfaced with only a single element.
    """
    elements = ['2']
    expected = ['2']
    actual = collapse(elements, center_element)

    assert expected == actual


def test_list_utils_collapse_multiple_elements(center_element):
    """
    Test that the elements are collapsed so that the max of each group of
    elements is surfaced when there are multiple elements that aren't the center
    element.
    """
    elements = ['1', '2', '2', '1', '3', '1']
    expected = ['2', '3']
    actual = collapse(elements, center_element)

    assert expected == actual


def test_list_utils_collapse_large_list(center_element):
    """
    Test that the elements are collapsed so that the max of each group of
    elements is surfaced when there are multiple elements that aren't the center
    element from a large list of elements.
    """
    elements = [
        '1', '2', '2', '1', '3', '1', '1', '1', '2', '2', '3', '3', '1', '3',
        '3', '4', '1', '1', '1', '4', '1', '4', '4', '4'
    ]
    expected = ['2', '3', '2', '3', '4', '4']
    actual = collapse(elements, center_element)

    assert expected == actual
