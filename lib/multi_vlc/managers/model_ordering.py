from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileDialog

from multi_vlc.const import ALLOWED_EXTENSIONS
from multi_vlc.qobjects.time_status_bar import changeStatusDec
from multi_vlc.vlc_model import Row
from multi_vlc.vlc_window.base import BaseWindow


class ModelManagement(BaseWindow):
    def __post_init__(self):
        super().__post_init__()

        self.actionAdd.triggered.connect(self.onAdd)
        self.actionDelete.triggered.connect(self.onDelete)
        self.actionMove_Up.triggered.connect(self.onMoveUp)
        self.actionMove_Down.triggered.connect(self.onMoveDown)

    @changeStatusDec(msg="Files added.")
    def onAdd(self):
        """Add selected files to model"""
        extensions = ' '.join(f'*.{ext}' for ext in ALLOWED_EXTENSIONS)
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
