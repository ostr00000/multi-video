import json
import os
import uuid
from dataclasses import dataclass, field, astuple, asdict
from typing import Tuple, List, Dict

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QRect
from multi_vlc.split_window import Position


@dataclass
class Row:
    files: List[str]
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (0, 0)
    factor_x: int = 1
    factor_y: int = 1
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


class VlcModel(QAbstractTableModel):
    COL_FILES = 0
    COL_POSITION = 1
    COL_SIZE = 2
    COL_FACTOR_X = 3
    COL_FACTOR_Y = 4
    COL_PID = 5
    COL_WID = 6

    headers = {
        COL_FILES: 'Files',
        COL_POSITION: 'Position (x, y)',
        COL_SIZE: 'Size (x, y)',
        COL_FACTOR_X: 'Factor x',
        COL_FACTOR_Y: 'Factor y',
        COL_PID: 'Process id',
        COL_WID: 'Window ids',
    }

    def __init__(self, *args):
        super().__init__(*args)
        self._data: List[Row] = [

        ]

    def flags(self, index: QModelIndex):
        fl = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() in (VlcModel.COL_FACTOR_X, VlcModel.COL_FACTOR_Y):
            fl |= Qt.ItemIsEditable
        return fl

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
        elif index.column() in (VlcModel.COL_FACTOR_X, VlcModel.COL_FACTOR_Y):
            return obj
        return str(obj)

    def setData(self, index: QModelIndex, value, role: int = ...):
        if role != Qt.EditRole:
            return False

        if index.column() == VlcModel.COL_FACTOR_X:
            self._data[index.row()].factor_x = value
        elif index.column() == VlcModel.COL_FACTOR_Y:
            self._data[index.row()].factor_y = value
        else:
            return False
        return True

    def moveRow(self, sourceParent: QModelIndex, sourceRow: int, destinationParent: QModelIndex,
                destinationChild: int):
        destinationRow = destinationChild + 1 if destinationChild > sourceRow else destinationChild
        self.beginMoveRows(sourceParent, sourceRow, sourceRow, destinationParent, destinationRow)
        row = self._data.pop(sourceRow)
        self._data.insert(destinationChild, row)
        self.endMoveRows()
        return True

    def appendRow(self, row: Row):
        i = len(self._data)
        self.beginInsertRows(QModelIndex(), i, i)
        self._data.append(row)
        self.endInsertRows()

    def removeRows(self, row: int, count: int, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        del self._data[row:row + count]
        self.endRemoveRows()
        return True

    def toJson(self):
        return json.dumps([d.toDict() for d in self._data], ensure_ascii=True)

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
