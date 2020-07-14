from typing import List

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QGridLayout

from multi_vlc.qobjects.widget.mpv_player import MpvPlayerWidget


class MpvPlayerGroupWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._players: List[MpvPlayerWidget] = []
        self._layout = QGridLayout(self)

    #     self.loop = asyncio.new_event_loop()
    #     self.thread = threading.Thread(target=self._loopRunner, daemon=True)
    #     self.thread.start()
    #
    # def _loopRunner(self):
    #     try:
    #         self.loop.run_forever()
    #     finally:
    #         self.loop.close()

    def createWidget(self, filename: str):
        # pl = MpvPlayerWidget(self, self.loop)
        pl = MpvPlayerWidget(self)
        self._players.append(pl)
        self._layout.addWidget(pl)
        pl.play(filename)

    def closeEvent(self, a0: QCloseEvent) -> None:
        for player in self._players:
            player.close()
        self._players.clear()

        # if self.loop.is_running():
        #     self.loop.call_soon_threadsafe(self.loop.stop)
        #
        # if self.thread.is_alive():
        #     self.thread.join(100)

        super().closeEvent(a0)

    def sizeHint(self) -> QSize:
        return QSize(600, 600)
