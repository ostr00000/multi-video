import logging
from typing import List, Dict

from PyQt5.QtCore import QSize, Qt, QEvent, QObject, pyqtProperty
from PyQt5.QtGui import QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QHBoxLayout

from multi_video.qobjects.settings import videoSettings
from multi_video.qobjects.widget.mpv_player import MpvPlayerWidget, ignoreShutdown
from multi_video.utils.split_window import calculatePosition, getMinimumRectangle
from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta

logger = logging.getLogger(__name__)


class _FrameWrapper(QFrame):
    def __init__(self, contentWidget: MpvPlayerWidget, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout(self)
        self._layout.addWidget(contentWidget)
        self._layout.setContentsMargins(0, 0, 0, 0)

        contentWidget.player.observe_property('mute', self.onMuteChanged)
        self._mute = contentWidget.player.mute
        self.setStyleSheet('QFrame[mute="false"]{ border:1px solid yellow; }')

    @ignoreShutdown
    def onMuteChanged(self, propertyName: str, propertyValue: bool):
        assert propertyName == 'mute'
        self._mute = propertyValue
        self.setStyleSheet(self.styleSheet())

    def getMute(self):
        return self._mute

    mute = pyqtProperty(bool, getMute)


class MpvPlayerGroupWidget(QWidget,
                           metaclass=GeometrySaverMeta.wrap(QWidget),
                           settings=videoSettings):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._players: Dict[int, MpvPlayerWidget] = {}

    def createSubWidgets(self, iterable):
        data = list(iterable)
        if not data:
            return

        rX, rY = getMinimumRectangle(data)
        positions = calculatePosition(data, rX, rY)
        for d in data:
            position = positions[d]
            position.nonNegativeSize()
            self.createSubWidget(position.posX, position.posY, position.sizeX, position.sizeY)

    def createSubWidget(self, row, column, rowSpan, columnSpan):
        pl = MpvPlayerWidget(self)
        fw = _FrameWrapper(pl, self)
        pl.installEventFilter(self)
        self._players[len(self._players)] = pl
        self._layout.addWidget(fw, row, column, rowSpan, columnSpan)

        logger.debug(f"Created player {id(pl)} [number={len(self._players)}]")

    def playInWidget(self, widgetNumber: int, filenames: List[str]):
        widget = self._players[widgetNumber]
        widget.play(filenames)

    def pause(self, isPause):
        for widget in self._players.values():
            widget.setPause(isPause)

    def closeEvent(self, a0: QCloseEvent) -> None:
        for player in self._players.values():
            player.close()

        self._players.clear()
        super().closeEvent(a0)

    def sizeHint(self) -> QSize:
        return QSize(600, 600)

    def eventFilter(self, obj: 'QObject', event: 'QEvent') -> bool:
        if isinstance(event, QMouseEvent):
            if event.button() == Qt.MidButton:
                if any((player := pl) is obj for pl in self._players.values()):
                    player.setMute(change=True)

        return super(MpvPlayerGroupWidget, self).eventFilter(obj, event)
