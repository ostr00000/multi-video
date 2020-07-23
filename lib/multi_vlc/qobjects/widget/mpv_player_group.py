from typing import List, Dict

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QGridLayout

from multi_vlc.qobjects.widget.mpv_player import MpvPlayerWidget
from multi_vlc.utils.split_window import calculatePosition, getMinimumRectangle


class MpvPlayerGroupWidget(QWidget):
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
            # print(position.posX, position.posY, position.sizeX, position.sizeY)
            self.createSubWidget(position.posX, position.posY, position.sizeX, position.sizeY)

    # def createSubWidget(self, position, size):
    def createSubWidget(self, row, column, rowSpan, columnSpan):
        pl = MpvPlayerWidget(self)
        self._players[len(self._players)] = pl
        # pl.move(*position)
        # pl.setFixedSize(*size)

        self._layout.addWidget(pl, row, column, rowSpan, columnSpan)

    def playInWidget(self, widgetNumber: int, filenames: List[str]):
        widget = self._players[widgetNumber]
        widget.play(filenames)

    def closeEvent(self, a0: QCloseEvent) -> None:
        for player in self._players.values():
            player.close()
        self._players.clear()
        super().closeEvent(a0)

    def sizeHint(self) -> QSize:
        return QSize(600, 600)
