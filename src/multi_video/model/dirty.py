from decorator import decorator
from PyQt5.QtCore import QAbstractTableModel, pyqtProperty, pyqtSignal


class DirtyModel(QAbstractTableModel):
    dirtyChanged = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dirty = False

    def _getDirty(self):
        return self._dirty

    def _setDirty(self, value: bool):
        if self._dirty is not value:
            self._dirty = value
            self.dirtyChanged.emit(value)

    isDirty = pyqtProperty(bool, _getDirty, _setDirty, notify=dirtyChanged)

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
