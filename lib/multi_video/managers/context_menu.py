import logging
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMenu, QAction

from multi_video.model.row import Row
from multi_video.window.base import BaseVideoWindow
from pyqt_utils.python.process_async import runProcessAsync

logger = logging.getLogger(__name__)


class OpenFileFolderAction(QAction):
    def __init__(self, filePath: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filePath = filePath
        self.triggered.connect(self.onTriggered)

    def onTriggered(self):
        runProcessAsync(f"xdg-open '{str(self.filePath.parent.absolute())}'")


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
        row: Row = index.data(self.model.RowRole)
        if not (row and row.files):
            return None

        menu = parentMenu.addMenu("Open file folder")
        for filePathStr in row.files:
            filePath = Path(filePathStr)
            action = OpenFileFolderAction(filePath, text=filePath.name, parent=menu)
            menu.addAction(action)
        return menu
