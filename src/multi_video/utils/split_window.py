import math
from dataclasses import dataclass
from typing import Iterable, Collection, Sized, TypeVar, Generator

from multi_video.qobjects.settings import videoSettings

_X = TypeVar('_X')


def tileGen(cx: int, cy: int) -> Iterable[tuple[int, int]]:
    """
    list(tileGen(2, 3))
    [(1, 2), (0, 2), (1, 1), (0, 1), (1, 0), (0, 0)]
    """
    for y in reversed(range(cy)):
        for x in reversed(range(cx)):
            yield x, y


def elementGen(elements: Iterable[_X], additional) -> Generator[_X, int, None]:
    """
    :param elements: iterable elements to be yielded
    :param additional: how many is additional positions, same element will be yield multiple times
    Expect to send how many positions left in current row after yield next element.
    Example:
        g = elementGen(list(range(100)), 5)
        next(g)
        val = [g.send(1) for i in range(20)]
        print(val[:5], val[5:10], val[10:15], val[15:])
        [0, 0, 1, 1, 2] [2, 3, 3, 4, 4] [5, 6, 7, 8, 9] [10, 11, 12, 13, 14]


        g = elementGen(list(range(100)), 5)
        next(g)
        val = [g.send(i % 5) for i in range(20)]
        print(val[:5], val[5:10], val[10:15], val[15:])
        [0, 1, 1, 2, 2] [3, 4, 4, 5, 5] [6, 7, 7, 8, 9] [10, 11, 12, 13, 14]

    """
    prevSize = yield
    for elem in elements:
        size = prevSize
        prevSize = yield elem
        if size > 0 and additional:
            prevSize = yield elem
            additional -= 1


@dataclass()
class Position:
    """
    Axes:  \n
    (0,0)  |  (1,0)  \n
    -------|------>  \n
    (1,0)  | (1,1)  \n
    """
    posX: int = 0
    posY: int = 0
    sizeX: int = 0
    sizeY: int = 0

    def move(self, x, y):
        self.posX += x
        self.posY += y

    def nonNegativeSize(self):
        if not self.sizeX:
            self.sizeX = 1

        if not self.sizeY:
            self.sizeY = 1


def getMinimumRectangle(elements: Sized):
    """
    (argument)->result
    (0)->(0, 0)
    (1)->(1, 1)
    (2)->(1, 2)
    (3)->(2, 2)
    (4)->(2, 2)
    (5)->(2, 3)
    (6)->(2, 3)
    (7)->(3, 3)
    (8)->(3, 3)
    """
    le = len(elements)
    s = int(math.sqrt(le))

    if le <= s * s:
        return s, s

    if le <= s * (s + 1):
        return s, s + 1

    if le <= (s + 1) * (s + 1):
        return s + 1, s + 1

    assert False


def getRectangle(elements: Sized):
    if (w := videoSettings.RECTANGLE_WIDTH) and (h := videoSettings.RECTANGLE_HEIGHT):
        return w, h
    return getMinimumRectangle(elements)


def calculatePosition(elements: Collection[_X],
                      width: int | None = None,
                      height: int | None = None) -> dict[_X, Position]:
    """Return map with elements mapped to Position"""
    cx, cy = getRectangle(elements)
    total = cx * cy
    additional = total - len(elements)

    xu = width / cx if width else 1
    yu = height / cy if height else 1

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
