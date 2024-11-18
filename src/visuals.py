"""Use matplotlib to render all you pretty things"""

from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

from utils import get_pattern_limits

r3o2 = np.sin(np.radians(60))
r3 = sqrt(3)


def plot_pattern(points):

    coord = [
        [0, 0, 0],
        [0, 1, -1],
        [-1, 1, 0],
        [-1, 0, 1],
        [0, -1, 1],
        [1, -1, 0],
        [1, 0, -1],
    ]

    # Horizontal cartesian coords
    vcoord = [-c[0] for c in points]

    # Vertical cartersian coords
    # vcoord = [2.0 * np.sin(np.radians(60)) * (c[1] - c[2]) / 3.0 for c in coord]
    # hcoord = [2.0 * np.sin(np.radians(60)) * (c[0] - c[2]) / 3.0 for c in coord] # good
    hcoord = [2 * c[1] * r3o2 / 3 for c in points]  # good

    min_r, min_c, max_r, max_c = get_pattern_limits(points)
    sf = max((max_r - min_r), ((max_c - min_c) * 2 * r3o2 / 3))
    sf = (10 / sf) ** 2

    fig, ax = plt.subplots(1)
    ax.set_aspect("equal")
    ax.axis("off")

    # Add some coloured hexagons
    for x, y in zip(hcoord, vcoord):
        hex = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=2.0 / 3.0,
            # radius=r3 / 2,
            # orientation=np.radians(30),
            facecolor="lightyellow",
            alpha=0.5,
            edgecolor="k",
        )
        ax.add_patch(hex)
        # Also add a text label
        # ax.text(x, y + 0.2, l[0], ha="center", va="center", size=20)

    # Also add scatter points in hexagon centres
    ax.scatter(hcoord, vcoord, c="k", s=sf)

    plt.show()


# plot_pattern()
