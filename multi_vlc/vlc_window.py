import logging
import os
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QEvent, QItemSelectionModel, QItemSelection, QModelIndex
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication
from util.commands import getRunningVlc
from multi_vlc.const import ALLOWED_EXTENSIONS
from util.decoators import SlotDecorator, changeStatusDec
from qobjects.process_controller import ProcessController
from qobjects.rubber_band_controller import RubberBandController
from qobjects.settings import settings
from util.split_window import calculatePosition, addOffsets
from qobjects.time_status_bar import TimeStatusBar
from multi_vlc.ui.ui_vlc import Ui_VlcMainWindow
from multi_vlc.vlc_model import VlcModel, Row

logger = logging.getLogger(__name__)


class VlcWindow(QMainWindow, RubberBandController, Ui_VlcMainWindow,
                metaclass=SlotDecorator):
    """Allow to configure position for multiple vlc instances"""

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.processController = ProcessController(self)
        self._connectButtons()
        self.setStatusBar(TimeStatusBar(self))

        self.model = VlcModel(self)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(VlcModel.COL_FILES, 400)

        self.lastJson = None
        path = settings.getLastFile()
        if path:
            self.loadConfiguration(path)

    def _connectButtons(self):
        self.actionNew.triggered.connect(self.onNew)
        self.actionSave_As.triggered.connect(self.onSaveAs)
        self.actionSave.triggered.connect(self.onSave)
        self.actionLoad.triggered.connect(self.onLoad)

        self.actionAdd.triggered.connect(self.onAdd)
        self.actionDelete.triggered.connect(self.onDelete)
        self.actionReset.triggered.connect(self.onReset)
        self.actionMove_Up.triggered.connect(self.onMoveUp)
        self.actionMove_Down.triggered.connect(self.onMoveDown)

        self.actionFind_Opened.triggered.connect(self.onFindOpened)
        self.actionSet_Position.triggered.connect(self.onSetPosition)
        self.actionAssign.triggered.connect(self.onRedistribute)

        self.actionStart.triggered.connect(self.processController.onStart)
        self.actionPause.triggered.connect(self.processController.onPause)
        self.actionClose.triggered.connect(self.processController.onStop)

    def event(self, event: QEvent):
        if event.type() == QEvent.WindowDeactivate:
            if isinstance(event, QMouseEvent):
                self.mousePressEvent(event)
                return True
        return super().event(event)

    @changeStatusDec(msg="Configuration loaded.")
    def loadConfiguration(self, path):
        try:
            with open(path) as file:
                jsonObj = file.read()
        except FileNotFoundError:
            settings.saveLastFile('')
            return

        self.lastJson = jsonObj
        self.model.loadJson(jsonObj)
        settings.saveLastFile(path)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent):
        """Accept only files"""
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()

    def dropEvent(self, a0: QtGui.QDropEvent):
        """Accept multiple files with ALLOWED_EXTENSIONS"""
        urls: List[QUrl] = a0.mimeData().urls()
        valid = []
        for url in urls:
            if url.scheme() != 'file':
                continue

            ext = os.path.splitext(url.path())[1][1:].lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue
            valid.append(url.path())
        if valid:
            self.model.appendRow(Row(valid))
            self.statusBar().showMessage("Files added.")

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.processController.onStop()
        # self.model.loadJson(self.model.toJson())
        super().closeEvent(a0)

    def onNew(self):
        """Create new model"""
        self.model.loadJson('[]')

    def onLoad(self):
        """Load model from file"""
        filePath, _ext = QFileDialog.getOpenFileName(
            self, "Load Configuration", filter="Configuration ( *.json )")
        if filePath:
            self.loadConfiguration(filePath)

    @changeStatusDec(msg="Configuration saved.")
    def onSave(self):
        """Save model to last file"""
        filePath = settings.getLastFile()
        if filePath:
            with open(filePath, 'w') as file:
                file.write(self.model.toJson())
            return True
        else:
            self.onSaveAs()

    @changeStatusDec(msg="Configuration saved.")
    def onSaveAs(self):
        """Save model to new file"""
        filePath, _ext = QFileDialog.getSaveFileName(
            self, "Save Configuration", filter="Configuration ( *.json )")
        if filePath:
            if not filePath.endswith('.json'):
                filePath += '.json'
            with open(filePath, 'w') as file:
                file.write(self.model.toJson())
            settings.saveLastFile(filePath)
            return True

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
        rows = self.tableView.selectionModel().selectedRows()
        if rows:
            for r in sorted(rows, key=lambda i: i.row(), reverse=True):  # type: QModelIndex
                self.model.removeRow(r.row())
            return True

    @changeStatusDec(msg="Configuration reset.")
    def onReset(self):
        """Reset configuration to last loaded"""
        if self.lastJson:
            self.model.loadJson(self.lastJson)
            return True
        else:
            QMessageBox.warning(self, "Cannot reset",
                                "To reset data must be loaded earlier")

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

    @changeStatusDec(msg="Found vlc instances.", failureMsg="Not found any vlc.")
    def onFindOpened(self):
        """Find processes vlc - look at '--started-from-file' option"""
        vlcFiles = getRunningVlc()
        for file in vlcFiles:
            self.model.appendRow(Row(files=[file]))
        return bool(vlcFiles)

    @changeStatusDec(msg="Position set.")
    def onSetPosition(self):
        """Activate screen rectangle selector"""
        ci = self.tableView.selectionModel().currentIndex()
        if not ci.isValid():
            s = self.model.index(0, 0)
            e = self.model.index(0, len(VlcModel.headers) - 1)
            selection = QItemSelection(s, e)
            self.tableView.selectionModel().select(selection, QItemSelectionModel.SelectCurrent)
            ci = self.tableView.selectionModel().currentIndex()
        if not ci.isValid():
            QMessageBox.warning(self, 'Not selected', 'None row is selected')
            self.actionSet_Position.setChecked(False)
            return

        self.rubberBandActive = True
        self.grabMouse()
        return True

    @changeStatusDec(msg="Configuration redistributed.")
    def onRedistribute(self):
        """Automatically set size and position for vlc"""
        data: List[Row] = list(iter(self.model))

        screen = QApplication.primaryScreen().availableGeometry()
        newPositions = calculatePosition(data, screen.width(), screen.height())
        addOffsets(screen.top(), screen.left(), *newPositions.values())

        self.model.setPositionAndSize(newPositions)
        return True
