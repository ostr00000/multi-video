import logging
import traceback
import types
from typing import Iterator, TypeVar

from PyQt5.QtCore import QObject, QCoreApplication, QAbstractTableModel, Qt
from decorator import decorator

_A = TypeVar('_A')
logger = logging.getLogger(__name__)


@decorator
def exceptionDec(fun, *args, **kwargs):
    try:
        return fun(*args, **kwargs)
    except Exception:
        logger.debug(str(traceback.format_exc()))
        raise


@decorator
def logDec(fun, *args, **kwargs):
    logger.debug(f"Run: {fun.__name__}")
    return fun(*args, **kwargs)


class SlotDecorator(type(QObject), type):
    def __new__(mcs, name, bases, namespace):
        for funName, fun in namespace.items():
            if isinstance(fun, types.FunctionType):
                if fun.__name__.startswith('on'):
                    namespace[funName] = exceptionDec(logDec(fun))

        return super().__new__(mcs, name, bases, namespace)


@decorator
def changeStatusDec(fun, msg: str = '', failureMsg='', *args, **kwargs):
    """
    None -> (skip decorator)
    False -> failureMsg
    _ -> msg
    """
    val = fun(*args, **kwargs)
    if val is False:
        msg = failureMsg
    elif val is None:
        return val

    self = args[0]
    try:
        statusBar = self.statusBar()
    except AttributeError:
        statusBar = self.parent().statusBar()

    statusBar.showMessage(msg)
    return val


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
