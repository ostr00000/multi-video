import json
import os
from dataclasses import dataclass, field, astuple, asdict
from typing import Tuple, List

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QRect


@dataclass
class Row:
    files: List[str]
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (0, 0)
    pid: int = -1
    wid: List[int] = field(default_factory=list)

    def toDict(self):
        d = asdict(self)
        del d['pid']
        del d['wid']
        return d


class VlcModel(QAbstractTableModel):
    headers = [
        'Files', 'Position (x, y)',
        'Size (x, y)', 'Process id', 'Window ids'
    ]

    def __init__(self, *args):
        super().__init__(*args)
        self._data: List[Row] = [

        ]

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
        if index.column() == 0:
            return ','.join(map(os.path.basename, obj))
        return str(obj)

    def addRow(self, files: List[str], **kwargs):
        i = len(self._data)
        self.beginInsertRows(QModelIndex(), i, i)
        self._data.append(Row(files, **kwargs))
        self.endInsertRows()

    def deleteRows(self, rows: List[QModelIndex]):
        internalRow = [r.row() for r in rows]
        internalRow.sort()
        for row in internalRow:
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._data[row]

        if internalRow:
            self.endRemoveRows()

    def toJson(self):
        return json.dumps([d.toDict() for d in self._data], ensure_ascii=True)

    def loadJson(self, jsonObj):
        self.beginResetModel()
        obj: List = json.loads(jsonObj)
        obj = [Row(d) for d in obj]
        self._data = obj
        self.endResetModel()

    def setPosition(self, index: QModelIndex, rectangle: QRect):
        r = index.row()
        row = self._data[r]
        row.position = (rectangle.x(), rectangle.y())
        row.size = (rectangle.width(), rectangle.height())
        self.dataChanged.emit(self.index(r, 0), self.index(r, 4))

    def __iter__(self):
        return iter(self._data)
