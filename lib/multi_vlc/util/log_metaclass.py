import logging
import traceback
import types

from PyQt5.QtCore import QObject
from decorator import decorator

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
