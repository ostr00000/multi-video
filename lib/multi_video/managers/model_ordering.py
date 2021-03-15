from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileDialog

from multi_video.model.row import Row
from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow
from pyqt_utils.python.time_status_bar import changeStatusDec


class ModelManagement(BaseVideoWindow):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)

        self.actionAdd.triggered.connect(self.onAdd)
        self.actionDelete.triggered.connect(self.onDelete)
        self.actionMove_Up.triggered.connect(self.onMoveUp)
        self.actionMove_Down.triggered.connect(self.onMoveDown)

    @changeStatusDec(msg="Files added.")
    def onAdd(self):
        """Add selected files to model"""
        extensions = ' '.join(f'*.{ext}' for ext in videoSettings.ALLOWED_EXTENSIONS)
        files, _ext = QFileDialog.getOpenFileNames(
            self, "Select files to open", filter=f"Films ({extensions})")
        if files:
            self.model.appendRow(Row(files))
            return True

    @changeStatusDec(msg="Rows deleted.")
    def onDelete(self):
        """Delete selected row"""
        if rows := self.tableView.selectionModel().selectedRows():
            for r in sorted(rows, key=lambda i: i.row(), reverse=True):  # type: QModelIndex
                self.model.removeRow(r.row())
            return True

    def onMoveUp(self):
        """Move record up"""
        self._moveRecord(-1)

    def onMoveDown(self):
        """Move record down"""
        self._moveRecord(1)

    @changeStatusDec(msg="Row moved.", failureMsg="No row selected.")
    def _moveRecord(self, delta: int):
        ci: QModelIndex = self.tableView.selectionModel().currentIndex()
        if not ci.isValid():
            return False

        rowNum = ci.row()
        newRowNum = rowNum + delta
        if 0 <= newRowNum < self.model.rowCount():
            self.model.moveRow(QModelIndex(), rowNum, QModelIndex(), newRowNum)
            return True
