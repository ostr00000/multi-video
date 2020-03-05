from typing import TypeVar, Iterator

from PyQt5.QtCore import QAbstractTableModel, Qt, QCoreApplication

_A = TypeVar('_A')


def dataChangeIterator(it: Iterator[_A], model: QAbstractTableModel, *columns: int) -> Iterator[_A]:
    for i, data in enumerate(it):
        yield data
        for column in columns:
            model.dataChanged.emit(
                model.index(i, column), model.index(i, column), (Qt.DisplayRole,))


def processEventsIterator(it: Iterator[_A]) -> Iterator[_A]:
    for i in it:
        QCoreApplication.instance().processEvents()
        yield i