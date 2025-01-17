import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps


def plotM(M, z):
    colors = colormaps["plasma"](np.linspace(0, 1, len(M)))
    fig, axs = plt.subplots(1, 2)
    for i in range(len(M)):
        axs[0].quiver(
            0,
            0,
            M[i, 0],
            M[i, 1],
            scale=2,
            color=colors[i],
        )
        axs[1].quiver(
            0,
            z[i],
            M[i, 0],
            M[i, 2],
            scale=5,
            color=colors[i],
        )
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("y")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("z")
    axs[0].set_aspect("equal")
    fig.suptitle(r"Magnetic moments after rotation by $\pi$ along $z$ axis")
    fig.tight_layout()


def plotM_animated(axs, M, z):
    colors = colormaps["plasma"](np.linspace(0, 1, len(M)))
    axs[0].clear()
    axs[1].clear()

    for i in range(len(M)):
        axs[0].quiver(
            0,
            0,
            M[i, 0],
            M[i, 1],
            scale=2,
            color=colors[i],
        )
        axs[1].quiver(
            0,
            z[i],
            M[i, 0],
            M[i, 2],
            scale=5,
            color=colors[i],
        )

    axs[0].set_xlabel("x")
    axs[0].set_ylabel("y")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("z")
    # axs[0].set_aspect("equal")

    axs[0].set_title("XY View")
    axs[1].set_title("XZ View")
