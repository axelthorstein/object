import sys
import warnings
import cv2
import numpy as np
from skimage import segmentation
from skimage import color
from skimage.future import graph
from profilehooks import timecall
from PIL.ImageFilter import SHARPEN
from PIL import Image


def _weight_mean_color(graph, src, dst, n):  #pylint: disable=unused-argument
    """Callback to handle merging nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.

    Args:
        graph (RAG): The graph under consideration.
        src (int): The vertices in `graph` to be merged.
        dst (int): The vertices in `graph` to be merged.
        n (int): A neighbor of `src` or `dst` or both.

    Returns:
        data (dict): A dictionary with the `"weight"` attribute set as the
            absolute difference of the mean color between node `dst` and `n`.
    """
    diff = graph.node[dst]['mean color'] - graph.node[n]['mean color']
    diff = np.linalg.norm(diff)

    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    """Callback called before merging two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.

    Args:
        graph (RAG): The graph under consideration.
        src (int): The vertices in `graph` to be merged.
        dst (int): The vertices in `graph` to be merged.
    """
    graph.node[dst]['total color'] += graph.node[src]['total color']
    graph.node[dst]['pixel count'] += graph.node[src]['pixel count']
    graph.node[dst]['mean color'] = (
        graph.node[dst]['total color'] / graph.node[dst]['pixel count'])


@timecall
def rag_merge_filter(image, filter_level=150):
    """Use the RAG merge filter algorithm to consolidate local pixel colors.

    Notes:
        The imput image must be RGB or this won't work.

    Args:
        image (numpy.ndarray): The image to filter.
        filter_level (int): The amount of merging that should be applied.

    Returns:
        numpy.ndarray: The filtered image.
    """
    image = np.asarray(image)
    labels = segmentation.slic(image, compactness=30, n_segments=640)
    g = graph.rag_mean_color(image, labels)

    labels2 = graph.merge_hierarchical(
        labels,
        g,
        thresh=filter_level,
        rag_copy=False,
        in_place_merge=True,
        merge_func=merge_mean_color,
        weight_func=_weight_mean_color)

    image = color.label2rgb(labels2, image, kind='avg')

    return Image.fromarray(image)


@timecall
def median_filter(image, blur_level=25):
    """Apply the median filter to an image to remove noise.

    Todo:
        Should avoid doing all this conversion. But using the PIL MedianFilter
        if multiple times slower than CV2.

    Args:
        image (Image): The image to filter.
        blur_level (int): The amount the image should be blurred.

    Returns:
        Image: The filtered image.
    """
    image = np.asarray(image)
    image = image[:, :, ::-1]  # Need to reverse the RGB to BGR for OpenCV.
    image = cv2.medianBlur(image, blur_level)  #pylint: disable=no-member

    return Image.fromarray(image[:, :, ::-1])  # Reverse back.


@timecall
def sharpen(image, sharpness=2):
    """Sharpen the edges in an image.

    Args:
        image (Image): The image to filter.
        sharpness (int): The number of times to sharpen the image.

    Returns:
        Image: The sharpened image.
    """
    for _ in range(sharpness):
        image = image.filter(SHARPEN)

    return image


if __name__ == '__main__':
    image_path = f'tests/test_images/{sys.argv[1]}.png'
    out_path = 'images/debug.png'

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        image = Image.open(image_path)

        image = rag_merge_filter(image)
        image = median_filter(image)
        image = sharpen(image)

        image.save(out_path)
