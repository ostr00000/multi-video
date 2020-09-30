import logging
from typing import List, Dict

from PyQt5.QtCore import QSize, Qt, QEvent, QObject
from PyQt5.QtGui import QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QWidget, QGridLayout

from multi_video.qobjects.settings import videoSettings
from multi_video.qobjects.widget.mpv_player import MpvPlayerWidget
from multi_video.utils.split_window import calculatePosition, getMinimumRectangle
from pyqt_settings.metaclass.geometry_saver import GeometrySaverMeta

logger = logging.getLogger(__name__)


class MpvPlayerGroupWidget(QWidget,
                           metaclass=GeometrySaverMeta.wrap(QWidget),
                           settings=videoSettings):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._layout = QGridLayout(self)
        self._players: Dict[int, MpvPlayerWidget] = {}

    def createSubWidgets(self, iterable):
        data = list(iterable)
        rX, rY = getMinimumRectangle(data)
        positions = calculatePosition(data, rX, rY)
        for d in data:
            position = positions[d]
            position.nonNegativeSize()
            self.createSubWidget(position.posX, position.posY, position.sizeX, position.sizeY)

    def createSubWidget(self, row, column, rowSpan, columnSpan):
        pl = MpvPlayerWidget(self)
        pl.installEventFilter(self)
        self._players[len(self._players)] = pl
        self._layout.addWidget(pl, row, column, rowSpan, columnSpan)

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
