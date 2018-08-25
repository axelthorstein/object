from skimage import io
from skimage import segmentation
from skimage import color
from skimage.future import graph
from cv2 import medianBlur
from cv2 import imwrite
from numpy.linalg import norm
from profilehooks import timecall


def _weight_mean_color(graph, src, dst, n):
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
    diff = norm(diff)
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
def rag_merge_filter(image_path, out_path):
    """Use the RAG merge filter algorithm to consolidate local pixel colors.

    Note:
        The imput image must be RGB or this won't work.

    Args:
        image_path (str): Path to the image.
        out_path (str): Path for the processed image to be written.
    """
    image = io.imread(image_path)
    labels = segmentation.slic(image, compactness=30, n_segments=640)
    g = graph.rag_mean_color(image, labels)

    labels2 = graph.merge_hierarchical(
        labels,
        g,
        thresh=35,
        rag_copy=False,
        in_place_merge=True,
        merge_func=merge_mean_color,
        weight_func=_weight_mean_color)

    out = color.label2rgb(labels2, image, kind='avg')
    image = out[:, :, ::-1] # Need to reverse the RGB to BGR for OpenCV. 
    image = medianBlur(image, 25)
    imwrite(out_path, image)


if __name__ == '__main__':
    image_path = 'tests/test_images/real_test_circle.png'
    out_path = 'images/debug.png'
    rag_merge_filter(image_path, out_path)
