from collections.abc import Iterator

from PyQt5.QtCore import QAbstractTableModel, QCoreApplication, Qt


def dataChangeIterator[A](
    it: Iterator[A], model: QAbstractTableModel, *columns: int
) -> Iterator[A]:
    for i, data in enumerate(it):
        yield data
        for column in columns:
            model.dataChanged.emit(
                model.index(i, column), model.index(i, column), (Qt.DisplayRole,)
            )


def processEventsIterator[A](it: Iterator[A]) -> Iterator[A]:
    if (app := QCoreApplication.instance()) is None:
        msg = "No QCoreApplication instance found"
        raise RuntimeError(msg)

    for i in it:
        app.processEvents()
        yield i
