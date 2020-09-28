from PyQt5 import QtGui

from multi_video.player.mpv import MpvPlayer
from multi_video.player.vlc import VlcPlayer
from multi_video.qobjects.settings import settings
from multi_video.qobjects.time_status_bar import changeStatusDec
from multi_video.window.base import BaseWindow


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

    @changeStatusDec(msg="Video paused.", failureMsg="Video resumed.")
    def onPause(self, isPause):
        return self._getPlayer().onPause(isPause)

    @changeStatusDec(msg="Video stopped.")
    def onStop(self):
        return self._getPlayer().onStop()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.onStop()
        super().closeEvent(a0)
