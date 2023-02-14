import base64
from io import BytesIO

from matplotlib import pyplot


def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


def get_plot(curves, mixture):
    pyplot.switch_backend("AGG")
    fig_size = (20 / 2.54, 20 / 2.54)
    pyplot.figure(figsize=fig_size)
    pyplot.title(f"Univolatility curves of {mixture} mixture")

    pyplot.plot([0, 1, 0, 0], [0, 0, 1, 0], "k", linewidth=1.5)
    for curve in curves:
        x1 = curve["x1"]
        x2 = curve["x2"]
        pyplot.plot(x1, x2)

    graph = get_graph()

    return graph
