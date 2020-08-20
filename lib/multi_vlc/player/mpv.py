import logging
from threading import Thread
from typing import Optional, List

from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication

from multi_vlc.player.base import BasePlayer
from multi_vlc.qobjects.widget.mpv_player_group import MpvPlayerGroupWidget
from multi_vlc.vlc_model import Row
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
        self._playerWidgetGroup.installEventFilter(self.baseWindow)
        self._playerWidgetGroup.destroyed.connect(self.onPlayerDestroyed)

        self._playerWidgetGroup.createSubWidgets(self.model)
        self._playerWidgetGroup.show()
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

        Thread(target=self._startPlayers, name='startPlayer',
               args=(list(self.model),), daemon=True).start()

        return True

    def _startPlayers(self, rows: List[Row]):
        try:
            for i, row in enumerate(rows):
                self._playerWidgetGroup.playInWidget(i, row.files)
                logger.debug(f'Start playing widget {i}')
        except (AttributeError, KeyError):
            logger.debug("user closed window while starting")

    def onPlayerDestroyed(self):
        self._playerWidgetGroup = None

    def onPause(self, isPause: bool):
        if self._playerWidgetGroup:
            if not isPause:
                self._playerWidgetGroup.raise_()
            self._playerWidgetGroup.pause(isPause)
            return isPause
        else:
            return

    def onStop(self):
        if self._playerWidgetGroup:
            self.baseWindow.actionPause.setChecked(False)
            self._playerWidgetGroup.close()
        return True
