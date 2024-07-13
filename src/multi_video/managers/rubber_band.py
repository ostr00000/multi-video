from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, QItemSelection, QItemSelectionModel, QPoint, QRect, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QMessageBox, QRubberBand, QToolButton
from pyqt_utils.python.late_init import LateInit
from pyqt_utils.widgets.time_status_bar_dec import changeStatusDec

from multi_video.model.video import VideoModel
from multi_video.window.base import BaseVideoWindow


class RubberBandManager(BaseVideoWindow):

    rubberBandActive = LateInit[bool]()
    rubberBand = LateInit[QRubberBand]()
    rubberBandStartPos = LateInit[QPoint](
        errorMsg="Rubber band is active, but start position is not set"
    )

    def __pre_init__(self, *args, **kwargs):
        super().__pre_init__(*args, **kwargs)
        self.rubberBandActive = False

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.actionSet_Position.triggered.connect(self.onSetPosition)

    @changeStatusDec(msg="Set position.")
    def onSetPosition(self):
        """Activate screen rectangle selector."""
        selMod = self.tableView.selectionModel()

        ci = selMod.currentIndex()
        if not ci.isValid():
            s = self.model.index(0, 0)
            e = self.model.index(0, len(VideoModel.headers) - 1)
            selection = QItemSelection(s, e)
            selMod.select(selection, QItemSelectionModel.SelectCurrent)
            ci = selMod.currentIndex()

        if not ci.isValid():
            QMessageBox.warning(self, 'Not selected', 'None row is selected')
            self.actionSet_Position.setChecked(False)
            return None

        self.rubberBandActive = True
        self.grabMouse()
        return True

    def event(self, event: QEvent):
        if event.type() == QEvent.WindowDeactivate and isinstance(event, QMouseEvent):
            self.mousePressEvent(event)
            return True

        return super().event(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self._onSetPositionClose()
            return

        super().keyPressEvent(event)

    def _onSetPositionClose(self):
        self.actionSet_Position.setChecked(False)
        self.rubberBandActive = False
        del self.rubberBand
        self.releaseMouse()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if not self.rubberBandActive:
            super().mousePressEvent(event)
            return

        child = self.childAt(event.pos())
        if (
            isinstance(child, QToolButton)
            and self.actionSet_Position in child.actions()
        ):
            self._onSetPositionClose()
            return

        if event.button() != Qt.LeftButton:
            del self.rubberBand
            return

        self.rubberBand = QRubberBand(QRubberBand.Rectangle)
        self.rubberBand.setGeometry(QRect())
        self.rubberBand.move(event.globalPos())
        self.rubberBand.show()
        self.rubberBandStartPos = event.globalPos()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        if not self.rubberBandActive:
            return super().mouseMoveEvent(a0)

        geom = QRect(self.rubberBandStartPos, a0.globalPos()).normalized()
        self.rubberBand.setGeometry(geom)
        return None

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.rubberBandActive:
            row = self.tableView.selectionModel().currentIndex()
            geom = QRect(self.rubberBandStartPos, a0.globalPos()).normalized()
            self.model.setPosition(row, geom)
            self._onSetPositionClose()

        super().mouseReleaseEvent(a0)
