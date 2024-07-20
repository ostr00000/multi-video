import json
import logging
from typing import ClassVar

from PyQt5.QtCore import QModelIndex, QRect, Qt

from multi_video.model.dirty import DirtyModel
from multi_video.model.row import BaseRow
from multi_video.utils.split_window import Position

logger = logging.getLogger(__name__)
_topModelIndex = QModelIndex()


class VideoModel(DirtyModel):
    COL_NAME = 0
    COL_POSITION = 1
    COL_SIZE = 2
    COL_PID = 3
    COL_WID = 4

    headers: ClassVar[dict[int, str]] = {
        COL_NAME: 'Files',
        COL_POSITION: 'Position (x, y)',
        COL_SIZE: 'Size (x, y)',
        COL_PID: 'Process id',
        COL_WID: 'Window ids',
    }

    RowRole = Qt.UserRole

    def __init__(self, *args):
        super().__init__(*args)
        self._data: list[BaseRow] = []

    def flags(self, index: QModelIndex):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, section: int, orientation: Qt.Orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return VideoModel.headers[section]
        return None

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(VideoModel.headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        row = self._data[index.row()]
        match role, index.column():
            case self.RowRole, _:
                return row
            case Qt.DisplayRole | Qt.ToolTipRole, VideoModel.COL_NAME:
                return str(row)
            case Qt.DisplayRole | Qt.ToolTipRole, VideoModel.COL_POSITION:
                return str(row.position)
            case Qt.DisplayRole, VideoModel.COL_SIZE:
                return str(row.size)
            case Qt.ToolTipRole, VideoModel.COL_SIZE:
                return f"Total files: {len(row.getFiles())}"

    @DirtyModel.dirtyDec
    def setData(self, index: QModelIndex, value, role: int = Qt.DisplayRole):
        if role != Qt.UserRole:
            return False

        self._data[index.row()].replace(index.column(), value)
        return True

    @DirtyModel.dirtyDec
    def moveRow(
        self,
        sourceParent: QModelIndex,
        sourceRow: int,
        destinationParent: QModelIndex,
        destinationChild: int,
    ):
        destinationRow = (
            destinationChild + 1 if destinationChild > sourceRow else destinationChild
        )
        self.beginMoveRows(
            sourceParent, sourceRow, sourceRow, destinationParent, destinationRow
        )
        row = self._data.pop(sourceRow)
        self._data.insert(destinationChild, row)
        self.endMoveRows()
        return True

    @DirtyModel.dirtyDec
    def appendRow(self, row: BaseRow):
        i = len(self._data)
        self.beginInsertRows(QModelIndex(), i, i)
        self._data.append(row)
        self.endInsertRows()

    @DirtyModel.dirtyDec
    def removeRows(self, row: int, count: int, parent=_topModelIndex):
        self.beginRemoveRows(parent, row, row + count - 1)
        del self._data[row : row + count]
        self.endRemoveRows()
        return True

    def clean(self):
        self.removeRows(0, len(self._data))

    @DirtyModel.cleanDec
    def toJson(self) -> str:
        return json.dumps([d.toDict() for d in self._data], ensure_ascii=True)

    @DirtyModel.cleanDec
    def loadJson(self, jsonObj: str):
        self.beginResetModel()

        obj = []
        for d in json.loads(jsonObj):
            try:
                obj.append(BaseRow.fromDict(d))
            except TypeError:
                logger.exception(f"Cannot convert {d} to {BaseRow}")

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

    def setPositionAndSize(self, newValues: dict[BaseRow, Position]):
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
