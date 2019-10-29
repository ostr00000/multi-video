import math
from dataclasses import dataclass
from pprint import pprint
from typing import List, Iterable, Collection, Sized, TypeVar, Generator, Tuple

_X = TypeVar('_X')


def tileGen(cx: int, cy: int) -> Iterable[Tuple[int, int]]:
    for y in reversed(range(cy)):
        for x in reversed(range(cx)):
            yield x, y


def elementGen(elements: Iterable[_X], additional) -> Generator[_X, int, None]:
    prevSize = yield
    for elem in elements:
        size = prevSize
        prevSize = yield elem
        if size > 0 and additional:
            prevSize = yield elem
            additional -= 1


@dataclass()
class Position:
    posX: int = 0
    posY: int = 0
    sizeX: int = 0
    sizeY: int = 0


def getCxCy(elements: Sized):
    le = len(elements)
    s = int(math.sqrt(le))

    if le <= s * s:
        return s, s

    if le <= s * (s + 1):
        return s, s + 1

    if le <= (s + 1) * (s + 1):
        return s + 1, s + 1

    assert False


def calculatePosition(elements: Collection[_X], x: int, y: int):
    cx, cy = getCxCy(elements)

    total = cx * cy
    additional = total - len(elements)
    xu = x / cx
    yu = y / cy

    result = {}
    eGen = elementGen(elements, additional)
    next(eGen)
    empty = Position()

    for posX, posY in tileGen(cx, cy):
        elemName = eGen.send(posX)
        elemPos = result.get(elemName, empty)
        pos = Position(int(posX * xu), int(posY * yu), int(elemPos.sizeX + xu), int(yu))
        result[elemName] = pos

    return result


def addOffsets(top: int, left: int, *elements: Position):
    for elem in elements:
        elem.posX += left
        elem.posY += top


if __name__ == '__main__':
    import matplotlib.patches as patches
    import matplotlib.pyplot as plt


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

    main()
