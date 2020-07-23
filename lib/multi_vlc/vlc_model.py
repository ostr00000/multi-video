import json
import os
import uuid
from dataclasses import dataclass, field, astuple, asdict
from typing import Tuple, List, Dict

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QRect, pyqtSignal, pyqtProperty
from decorator import decorator

from multi_vlc.utils.split_window import Position


class Enum:
    @classmethod
    def getDict(cls):
        return {k: v for k, v in cls.__dict__.items()
                if k.islower() and not k.startswith('_')}


@dataclass
class DataClass(Enum):
    def replace(self, index: int, val):
        k, v = list(self.getDict())[index]
        setattr(self, k, val)


@dataclass
class Row(DataClass):
    files: List[str]
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (0, 0)
    pid: int = -1
    wid: List[int] = field(default_factory=list)
    hashId: str = field(default_factory=lambda: uuid.uuid4().__str__())

    def __hash__(self):
        return hash(self.hashId)

    def toDict(self):
        d = asdict(self)
        del d['pid']
        del d['wid']
        return d


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


class VlcModel(DirtyModel):
    COL_FILES = 0
    COL_POSITION = 1
    COL_SIZE = 2
    COL_PID = 3
    COL_WID = 4

    headers = {
        COL_FILES: 'Files',
        COL_POSITION: 'Position (x, y)',
        COL_SIZE: 'Size (x, y)',
        COL_PID: 'Process id',
        COL_WID: 'Window ids',
    }

    def __init__(self, *args):
        super().__init__(*args)
        self._data: List[Row] = []

    def flags(self, index: QModelIndex):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, section: int, orientation: Qt.Orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return VlcModel.headers[section]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(VlcModel.headers)

    def data(self, index: QModelIndex, role: int = ...):
        if role not in (Qt.DisplayRole, Qt.ToolTipRole):
            return

        row = self._data[index.row()]
        obj = astuple(row)[index.column()]
        if index.column() == VlcModel.COL_FILES:
            return ','.join(map(os.path.basename, obj))

        return str(obj)

    @DirtyModel.dirtyDec
    def setData(self, index: QModelIndex, value, role: int = ...):
        if role != Qt.UserRole:
            return False

        self._data[index.row()].replace(index.column(), value)
        return True

    @DirtyModel.dirtyDec
    def moveRow(self, sourceParent: QModelIndex, sourceRow: int, destinationParent: QModelIndex,
                destinationChild: int):
        destinationRow = destinationChild + 1 if destinationChild > sourceRow else destinationChild
        self.beginMoveRows(sourceParent, sourceRow, sourceRow, destinationParent, destinationRow)
        row = self._data.pop(sourceRow)
        self._data.insert(destinationChild, row)
        self.endMoveRows()
        return True

    @DirtyModel.dirtyDec
    def appendRow(self, row: Row):
        i = len(self._data)
        self.beginInsertRows(QModelIndex(), i, i)
        self._data.append(row)
        self.endInsertRows()

    @DirtyModel.dirtyDec
    def removeRows(self, row: int, count: int, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        del self._data[row:row + count]
        self.endRemoveRows()
        return True

    def clean(self):
        self.removeRows(0, len(self._data))

    @DirtyModel.cleanDec
    def toJson(self):
        return json.dumps([d.toDict() for d in self._data], ensure_ascii=True)

    @DirtyModel.cleanDec
    def loadJson(self, jsonObj):
        self.beginResetModel()
        obj: List = json.loads(jsonObj)
        obj = [Row(**d) for d in obj]
        self._data = obj
        self.endResetModel()

    def setPosition(self, index: QModelIndex, rectangle: QRect):
        r = index.row()
        row = self._data[r]
        row.position = (rectangle.x(), rectangle.y())
        row.size = (rectangle.width(), rectangle.height())

        s = self.index(r, 0)
        e = self.index(r, len(self.headers))
        self.dataChanged.emit(s, e)

    def setPositionAndSize(self, newValues: Dict[Row, Position]):
        self.beginResetModel()

        for row in self._data:
            newValue = newValues[row]
            row.position = newValue.posX, newValue.posY
            row.size = newValue.sizeX, newValue.sizeY

        self.endResetModel()

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)
