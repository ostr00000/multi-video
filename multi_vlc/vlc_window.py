import logging
import os
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QObject, QEvent, QItemSelectionModel, QItemSelection, QModelIndex, QThread
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QMessageBox

from multi_vlc.commands import getRunningVlc, resizeAndMove, getWid
from multi_vlc.decoators import SlotDecorator
from multi_vlc.process_controller import ProcessController
from multi_vlc.rubber_band_controller import RubberBandController
from multi_vlc.settings import settings
from multi_vlc.ui.ui_vlc import Ui_VlcMainWindow
from multi_vlc.vlc_model import VlcModel, Row

logger = logging.getLogger(__name__)


class MouseFilter(QObject):

    def __init__(self, *args):
        super().__init__(*args)

    def eventFilter(self, a0: 'QWidget', a1: 'QEvent'):
        if a1.type() == QEvent.WindowDeactivate:
            if isinstance(a1, QMouseEvent):
                a0.mousePressEvent(a1)
                return True
        return super().eventFilter(a0, a1)


class VlcWindow(QMainWindow, RubberBandController, Ui_VlcMainWindow,
                metaclass=SlotDecorator):
    """Allow to configure position for multiple vlc instances"""

    ALLOWED_EXT = ('mp4', 'webm', 'avi')

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.installEventFilter(MouseFilter(self))

        self.actionAdd.triggered.connect(self.onAdd)
        self.actionDelete.triggered.connect(self.onDelete)
        self.actionReset.triggered.connect(self.onReset)
        self.actionLoad.triggered.connect(self.onLoad)
        self.actionSave.triggered.connect(self.onSave)
        self.actionSave_As.triggered.connect(self.onSaveAs)
        self.actionFind_Opened.triggered.connect(self.onFindOpened)
        self.actionSet_Position.triggered.connect(self.onSetPosition)
        self.actionStart.triggered.connect(self.onStart)
        self.actionPause.triggered.connect(self.onPause)
        self.actionClose.triggered.connect(self.onClose)

        self.model = VlcModel(self)
        self.tableView.setModel(self.model)
        self.processController = ProcessController()
        self.lastJson = None
        path = settings.getLastFile()
        if path:
            self.loadConfiguration(path)

    def loadConfiguration(self, path):
        with open(path) as file:
            jsonObj = file.read()

        self.lastJson = jsonObj
        self.model.loadJson(jsonObj)
        settings.saveLastFile(path)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent):
        """Accept only files"""
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()

    def dropEvent(self, a0: QtGui.QDropEvent):
        """Accept multiple files with ALLOWED_EXTension"""
        urls: List[QUrl] = a0.mimeData().urls()
        valid = []
        for url in urls:
            if url.scheme() != 'file':
                continue

            ext = os.path.splitext(url.path())[1][1:].lower()
            if ext not in self.ALLOWED_EXT:
                continue
            valid.append(url.path())
        if valid:
            self.model.appendRow(Row(valid))

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.onClose()
        super().closeEvent(a0)

    def onAdd(self):
        """Add selected files to model"""
        extensions = ' '.join(f'*.{ext}' for ext in self.ALLOWED_EXT)
        files, _ext = QFileDialog.getOpenFileNames(
            self, "Select files to open", filter=f"Films ({extensions})")
        if files:
            self.model.appendRow(Row(files))

    def onDelete(self):
        """Delete selected row"""
        rows = self.tableView.selectionModel().selectedRows()
        if rows:
            for r in rows:  # type: QModelIndex
                self.model.removeRow(r.row())

    def onReset(self):
        """Reset configuration to last loaded"""
        if self.lastJson:
            self.model.loadJson(self.lastJson)
        else:
            QMessageBox.warning(self, "Cannot reset",
                                "To reset data must be loaded earlier")

    def onLoad(self):
        """Load model from file"""
        filePath, _ext = QFileDialog.getOpenFileName(
            self, "Load Configuration", filter="Configuration ( *.json )")
        if filePath:
            self.loadConfiguration(filePath)

    def onSave(self):
        """Save model to last file"""
        filePath = settings.getLastFile()
        with open(filePath, 'w') as file:
            file.write(self.model.toJson())

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

    def onFindOpened(self):
        """Find processes vlc - look at '--started-from-file' option"""
        vlcProcesses = getRunningVlc()
        for process in vlcProcesses:
            pid = process[0]
            self.model.appendRow(Row(process[1], pid=pid))

    def onSetPosition(self):
        """Activate screen rectangle selector"""
        rows = self.tableView.selectionModel().selectedRows()
        if not rows:
            selection = QItemSelection(self.model.index(0, 0), self.model.index(0, 4))
            self.tableView.selectionModel().select(selection, QItemSelectionModel.Select)
            rows = self.tableView.selectionModel().selectedRows()
        if not rows:
            QMessageBox.warning(self, 'Not selected', 'None row is selected')
            self.actionSet_Position.setChecked(False)
            return

        self.rubberBandActive = True
        self.grabMouse()

    def onStart(self):
        """Run model files in vlc processes"""
        running = self.processController.isRunning()
        self.onClose()
        if running:
            QThread.sleep(1)

        self.model.beginResetModel()
        try:
            allWid = set(getWid())
            for row in self.model:
                row.pid = self.processController.run(row)
                QThread.sleep(1)
                newerWid = set(getWid())
                row.wid = list(newerWid - allWid)
                allWid = newerWid
                resizeAndMove(row)
        except ValueError as er:
            logger.error(er)
        self.model.endResetModel()

        QThread.sleep(1)
        self.onPause(isPause=True)
        self.actionPause.setChecked(True)

    def onPause(self, isPause):
        """Toggle pause of all vlc"""
        self.processController.setPause(isPause)

    def onClose(self):
        """Close all vlc processes"""
        self.actionPause.setChecked(False)
        self.processController.terminate()


def main():
    logging.basicConfig()
    mainLogger = logging.getLogger('multi_vlc')
    mainLogger.setLevel(logging.DEBUG)

    app = QApplication([])
    vw = VlcWindow()
    vw.show()
    app.exec()


if __name__ == '__main__':
    main()
