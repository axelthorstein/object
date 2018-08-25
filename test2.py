from skimage import data, io, segmentation, color
from skimage.filters import rank
from skimage.future import graph
from skimage.color import rgba2rgb
from skimage.morphology import watershed, disk

import numpy as np


def _weight_mean_color(graph, src, dst, n):
    """Callback to handle merging nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    data : dict
        A dictionary with the `"weight"` attribute set as the absolute
        difference of the mean color between node `dst` and `n`.
    """

    diff = graph.node[dst]['mean color'] - graph.node[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    """Callback called before merging two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    """
    graph.node[dst]['total color'] += graph.node[src]['total color']
    graph.node[dst]['pixel count'] += graph.node[src]['pixel count']
    graph.node[dst]['mean color'] = (
        graph.node[dst]['total color'] / graph.node[dst]['pixel count'])


# img = rgba2rgb(io.imread('tests/test_images/real_test_circle.png'))
img = io.imread('tests/test_images/real_test_circle_rgb.png')
# img = io.imread('tests/test_images/circle_thick_18_round.png')
# img = io.imread('images/debug.png')
# img = data.coffee()
labels = segmentation.slic(img, compactness=30, n_segments=640)
g = graph.rag_mean_color(img, labels)

labels2 = graph.merge_hierarchical(
    labels,
    g,
    thresh=35,
    rag_copy=False,
    in_place_merge=True,
    merge_func=merge_mean_color,
    weight_func=_weight_mean_color)

out = color.label2rgb(labels2, img, kind='avg')
io.imsave('images/debug.png', out)

import cv2
image = cv2.imread('images/debug.png')
processed_image = cv2.medianBlur(image, 25)
cv2.imwrite('images/debug.png', processed_image)
