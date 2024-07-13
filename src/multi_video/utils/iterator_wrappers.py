from collections.abc import Iterator
from typing import TypeVar

from PyQt5.QtCore import QAbstractTableModel, QCoreApplication, Qt

_A = TypeVar('_A')


def dataChangeIterator(
    it: Iterator[_A], model: QAbstractTableModel, *columns: int
) -> Iterator[_A]:
    for i, data in enumerate(it):
        yield data
        for column in columns:
            model.dataChanged.emit(
                model.index(i, column), model.index(i, column), (Qt.DisplayRole,)
            )


def processEventsIterator(it: Iterator[_A]) -> Iterator[_A]:
    if (app := QCoreApplication.instance()) is None:
        msg = "No QCoreApplication instance found"
        raise RuntimeError(msg)

    for i in it:
        app.processEvents()
        yield i
