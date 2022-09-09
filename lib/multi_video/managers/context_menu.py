from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMenu

from multi_video.model.row import BaseRow
from multi_video.window.base import BaseVideoWindow


class ContextMenuManager(BaseVideoWindow):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onCustomContextMenuRequested)

    def onCustomContextMenuRequested(self, pos: QPoint):
        globalPos = self.mapToGlobal(pos)
        menu = QMenu(parent=self)
        self._getOpenFileMenu(globalPos, menu)
        menu.exec(globalPos)
        menu.deleteLater()

    def _getOpenFileMenu(self, globalPos: QPoint, parentMenu: QMenu):
        pos = self.tableView.viewport().mapFromGlobal(globalPos)
        index = self.tableView.indexAt(pos)
        row: BaseRow = index.data(self.model.RowRole)
        if not row:
            return None

        row.prepareContextMenu(parentMenu)
