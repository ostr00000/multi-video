from PyQt5.QtCore import QAbstractTableModel, pyqtSignal, pyqtProperty
from decorator import decorator


class DirtyModel(QAbstractTableModel):
    dirtyChanged = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dirty = False

    def getDirty(self):
        return self._dirty

    def setDirty(self, value: bool):
        if self._dirty is not value:
            self._dirty = value
            self.dirtyChanged.emit(value)

    isDirty = pyqtProperty(bool, getDirty, setDirty, notify=dirtyChanged)

    @staticmethod
    @decorator
    def dirtyDec(fun, *args, **kwargs):
        args[0].isDirty = True
        return fun(*args, **kwargs)

    @staticmethod
    @decorator
    def cleanDec(fun, *args, **kwargs):
        args[0].isDirty = False
        return fun(*args, **kwargs)
