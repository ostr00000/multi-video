import logging
from threading import Thread

from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication

from multi_video.model.row import BaseRow
from multi_video.player.base import BasePlayer
from multi_video.qobjects.widget.mpv_player_group import MpvPlayerGroupWidget
from multi_video.window.base import BaseVideoWindow

logger = logging.getLogger(__name__)


class MpvPlayer(BasePlayer):

    def __init__(self, baseWindow: BaseVideoWindow, *args):
        super().__init__(baseWindow, *args)
        self._playerWidgetGroup: MpvPlayerGroupWidget | None = None

    def onStart(self):
        if self._playerWidgetGroup is not None:
            self._playerWidgetGroup.raise_()
            self._playerWidgetGroup.pause(isPause=False)
            self.baseWindow.actionPause.setChecked(False)
            return None

        self._playerWidgetGroup = MpvPlayerGroupWidget()
        self._playerWidgetGroup.installEventFilter(self.baseWindow)
        self._playerWidgetGroup.destroyed.connect(self.onPlayerDestroyed)

        self._playerWidgetGroup.createSubWidgets(self.model)
        self._playerWidgetGroup.show()
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

        Thread(
            target=self._startPlayers,
            name='startPlayer',
            args=(list(self.model),),
            daemon=True,
        ).start()

        return True

    def _startPlayers(self, rows: list[BaseRow]):
        if self._playerWidgetGroup is None:
            return

        try:
            for i, row in enumerate(rows):
                if files := row.getFiles():
                    self._playerWidgetGroup.playInWidget(i, files)
                    logger.debug(f'Start playing widget {i}')
                else:
                    logger.debug(f'Skipping widget {i} - no files')
        except (AttributeError, KeyError):
            logger.debug("user closed window while starting")

    def onPlayerDestroyed(self):
        self._playerWidgetGroup = None

    def onPause(self, isPause) -> bool | None:
        if self._playerWidgetGroup is None:
            self.baseWindow.actionPause.setChecked(False)
            return None

        self.baseWindow.actionPause.setChecked(isPause)
        if not isPause:
            self._playerWidgetGroup.raise_()
        self._playerWidgetGroup.pause(isPause=isPause)
        return isPause

    def onStop(self) -> bool:
        if self._playerWidgetGroup is not None:
            self.baseWindow.actionPause.setChecked(False)
            self._playerWidgetGroup.close()
        return True
