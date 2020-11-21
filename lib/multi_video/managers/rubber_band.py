from typing import Optional

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt, QRect, QItemSelection, QItemSelectionModel, QEvent
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QRubberBand, QToolButton, QMessageBox

from multi_video.model.video import VideoModel
from multi_video.window.base import BaseWindow
from pyqt_utils.python.time_status_bar import changeStatusDec


class RubberBandManager(BaseWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.rubberBand: Optional[QRubberBand] = None
        self.rubberBandActive = False
        self.rubberBandStartPos: Optional[QPoint] = None

    def __post_init__(self):
        super().__post_init__()

        self.actionSet_Position.triggered.connect(self.onSetPosition)

    @changeStatusDec(msg="Set position.")
    def onSetPosition(self):
        """Activate screen rectangle selector"""
        ci = self.tableView.selectionModel().currentIndex()
        if not ci.isValid():
            s = self.model.index(0, 0)
            e = self.model.index(0, len(VideoModel.headers) - 1)
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

    def event(self, event: QEvent):
        if event.type() == QEvent.WindowDeactivate:
            if isinstance(event, QMouseEvent):
                self.mousePressEvent(event)
                return True
        return super().event(event)

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == Qt.Key_Escape:
            self._onSetPositionClose()
        else:
            super().keyPressEvent(a0)

    def _onSetPositionClose(self):
        self.actionSet_Position.setChecked(False)
        self.rubberBandActive = False
        self.rubberBand = None
        self.releaseMouse()

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        if not self.rubberBandActive:
            super().mousePressEvent(a0)
            return

        child = self.childAt(a0.pos())
        if isinstance(child, QToolButton):
            if self.actionSet_Position in child.actions():
                self._onSetPositionClose()
                return

        if a0.button() != Qt.LeftButton:
            self.rubberBand = None
            return

        self.rubberBand = QRubberBand(QRubberBand.Rectangle)
        self.rubberBand.setGeometry(QRect())
        self.rubberBand.move(a0.globalPos())
        self.rubberBand.show()
        self.rubberBandStartPos = a0.globalPos()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        if self.rubberBandActive and self.rubberBand:
            geom = QRect(self.rubberBandStartPos, a0.globalPos()).normalized()
            self.rubberBand.setGeometry(geom)
        else:
            return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.rubberBandActive and self.rubberBand:
            row = self.tableView.selectionModel().currentIndex()
            geom = QRect(self.rubberBandStartPos, a0.globalPos()).normalized()
            self.model.setPosition(row, geom)
            self._onSetPositionClose()

        super().mouseReleaseEvent(a0)
