from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches

from multi_video.utils.split_window import Position, calculatePosition


def draw(data: list[Position], dimX, dimY):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')

    total = len(data)
    for a, pos in enumerate(data):
        ax.add_patch(
            patches.Rectangle(
                (pos.posX, pos.posY), pos.sizeX, pos.sizeY, alpha=(a / total)
            )
        )

    plt.xlim((0, dimX))
    plt.ylim((dimY, 0))

    outDirPath = Path('out')
    outDirPath.mkdir(parents=True, exist_ok=True)
    outFilePath = outDirPath / f't{len(data)}.png'
    plt.savefig(outFilePath)


def main():
    for i in range(1, 17):
        a = list(range(i))
        x = 1600
        y = 1200
        r = calculatePosition(a, x, y)
        val = list(r.values())
        draw(val, x, y)


if __name__ == '__main__':
    main()
