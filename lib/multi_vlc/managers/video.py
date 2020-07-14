from PyQt5 import QtGui

from multi_vlc.player.mpv import MpvPlayer
from multi_vlc.player.vlc import VlcPlayer
from multi_vlc.qobjects.settings import settings
from multi_vlc.qobjects.time_status_bar import changeStatusDec
from multi_vlc.vlc_window.base import BaseWindow


class VideoManager(BaseWindow):
    def __post_init__(self):
        super().__post_init__()
        self.vlc = VlcPlayer(self)
        self.mpv = MpvPlayer(self)

        self.actionStart.triggered.connect(self.onStart)
        self.actionPause.triggered.connect(self.onPause)
        self.actionClose.triggered.connect(self.onStop)

    def _getPlayer(self):
        player = getattr(self, settings.VIDEO_PLAYER)
        return player

    @changeStatusDec(msg="Video started.")
    def onStart(self):
        return self._getPlayer().onStart()

    @changeStatusDec(msg="Video paused.", failureMsg="Vlc resumed.")
    def onPause(self, isPause, process=None):
        return self._getPlayer().onPause(isPause, process)

    @changeStatusDec(msg="Video stopped.")
    def onStop(self):
        return self._getPlayer().onStop()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.onStop()
        super().closeEvent(a0)
