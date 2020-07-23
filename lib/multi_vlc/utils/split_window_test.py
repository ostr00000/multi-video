import os
from pprint import pprint
from typing import List

import matplotlib.patches as patches
import matplotlib.pyplot as plt

from multi_vlc.utils.split_window import calculatePosition, Position


def draw(data: List[Position], dimX, dimY):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')

    total = len(data)
    for a, pos in enumerate(data):
        ax.add_patch(patches.Rectangle(
            (pos.posX, pos.posY), pos.sizeX, pos.sizeY,
            alpha=(a / total)))

    plt.xlim((0, dimX))
    plt.ylim((dimY, 0))
    os.makedirs('out', exist_ok=True)
    plt.savefig(f'out/t{len(data)}.png')


def main():
    for i in range(1, 17):
        a = list(range(i))
        x = 1600
        y = 1200
        r = calculatePosition(a, x, y)
        val = list(r.values())
        pprint(r)
        draw(val, x, y)


if __name__ == '__main__':
    main()
