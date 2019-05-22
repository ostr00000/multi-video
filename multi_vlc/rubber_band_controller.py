from typing import Optional

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QRubberBand, QWidget, QToolButton


class RubberBandController(QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.grabKeyboard()
        self.rubberBand: Optional[QRubberBand] = None
        self.rubberBandActive = False
        self.rubberBandStartPos: Optional[QPoint] = None

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

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.rubberBandActive and self.rubberBand:
            row = self.tableView.selectionModel().selectedRows()[0]
            geom = QRect(self.rubberBandStartPos, a0.globalPos()).normalized()
            self.model.setPosition(row, geom)
            self._onSetPositionClose()
