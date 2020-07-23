import logging
from typing import Optional

from PyQt5.QtCore import QEventLoop, QTimer

from multi_vlc.player.base import BasePlayer
from multi_vlc.qobjects.widget.mpv_player_group import MpvPlayerGroupWidget
from multi_vlc.vlc_window.base import BaseWindow

logger = logging.getLogger(__name__)


class MpvPlayer(BasePlayer):

    def __init__(self, baseWindow: BaseWindow, *args):
        super().__init__(baseWindow, *args)
        self._playerWidgetGroup: Optional[MpvPlayerGroupWidget] = None

    def onStart(self):
        if self._playerWidgetGroup:
            self._playerWidgetGroup.raise_()
            return

        self._playerWidgetGroup = MpvPlayerGroupWidget()
        self._playerWidgetGroup.destroyed.connect(self.onPlayerDestroyed)

        self._playerWidgetGroup.createSubWidgets(self.model)
        # for i, row in enumerate(self.model):  # type: (int, Row)
        #     self._playerWidgetGroup.createSubWidget(row.position, row.size)

        self._waitForPlayerReady()
        self._playerWidgetGroup.show()
        self._waitForPlayerReady()
        for i, row in enumerate(self.model):
            self._playerWidgetGroup.playInWidget(i, row.files)

    @staticmethod
    def _waitForPlayerReady():
        ev = QEventLoop()
        QTimer.singleShot(500, ev.quit)
        ev.exec_()

    def onPlayerDestroyed(self):
        self._playerWidgetGroup = None

    def onPause(self, isPause: bool):
        pass

    def onStop(self):
        if self._playerWidgetGroup:
            self._playerWidgetGroup.close()
