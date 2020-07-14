import logging
from typing import Optional

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

        for row in self.model:  # type: Row
            file = row.files[0]
            self._playerWidgetGroup.createWidget(file)

        self._playerWidgetGroup.showMaximized()

    def onPause(self, isPause: bool):
        pass

    def onStop(self):
        if self._playerWidgetGroup:
            self._playerWidgetGroup.close()
            self._playerWidgetGroup.deleteLater()
            self._playerWidgetGroup = None
