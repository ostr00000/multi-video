import os
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, QObject, QEvent, QItemSelectionModel, QItemSelection
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QMessageBox

from multi_vlc.commands import getRunningVlc, getWidFromPid
from multi_vlc.process_controller import ProcessController
from multi_vlc.rubber_band_controller import RubberBandController
from multi_vlc.ui.ui_vlc import Ui_VlcMainWindow
from multi_vlc.vlc_model import VlcModel


class MouseFilter(QObject):

    def __init__(self, *args):
        super().__init__(*args)

    def eventFilter(self, a0: 'QWidget', a1: 'QEvent'):
        if a1.type() == QEvent.WindowDeactivate:
            a0.mousePressEvent(a1)
            return True
        return super().eventFilter(a0, a1)


class VlcWindow(QMainWindow, RubberBandController, Ui_VlcMainWindow):
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
        self.actionFind_Opened.triggered.connect(self.onFindOpened)
        self.actionSet_Position.triggered.connect(self.onSetPosition)
        self.actionStart.triggered.connect(self.onStart)
        self.actionPause.triggered.connect(self.onPause)
        self.actionClose.triggered.connect(self.onClose)

        self.model = VlcModel(self)
        self.tableView.setModel(self.model)
        self.processController = ProcessController()

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
            self.model.addRow(valid)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.onClose()
        super().closeEvent(a0)

    def onAdd(self):
        """Add selected files to model"""
        extensions = ' '.join(f'*.{ext}' for ext in self.ALLOWED_EXT)
        files, _ext = QFileDialog.getOpenFileNames(
            self, "Select files to open", filter=f"Films ({extensions})")
        if files:
            self.model.addRow(files)

    def onDelete(self):
        """Delete selected row"""
        rows = self.tableView.selectionModel().selectedRows()
        if rows:
            self.model.deleteRows(rows)

    def onReset(self):
        """Reset configuration to last loaded"""
        raise NotImplementedError  # TODO QUndoStack

    def onLoad(self):
        """Load model from file"""
        fileName, _ext = QFileDialog.getOpenFileName(
            self, "Load Configuration", filter="Configuration ( *.json )")
        if fileName:
            with open(fileName) as file:
                jsonObj = file.read()
            self.model.loadJson(jsonObj)

    def onSave(self):
        """Save model to file"""
        fileName, _ext = QFileDialog.getSaveFileName(
            self, "Save Configuration", filter="Configuration ( *.json )")
        if fileName:
            if not fileName.endswith('.json'):
                fileName += '.json'
            with open(fileName, 'w') as file:
                file.write(self.model.toJson())

    def onFindOpened(self):
        """Find processes vlc - look at '--started-from-file' option"""
        vlcProcesses = getRunningVlc()
        for process in vlcProcesses:
            pid = process[0]
            wid = getWidFromPid(pid)
            self.model.addRow(process[1], pid=pid, wid=wid)

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
        for row in self.model:
            self.processController.run(row)

    def onPause(self, isPause):
        """Toggle pause of all vlc"""
        self.processController.setPause(isPause)

    def onClose(self):
        """Close all vlc processes"""
        self.processController.terminate()


def main():
    app = QApplication([])
    vw = VlcWindow()
    vw.show()
    app.exec()


if __name__ == '__main__':
    main()
