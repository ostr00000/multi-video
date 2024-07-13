from PyQt5 import QtGui
from pyqt_utils.widgets.time_status_bar_dec import changeStatusDec

from multi_video.player.mpv import MpvPlayer
from multi_video.player.vlc import VlcPlayer
from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow


class VideoManager(BaseVideoWindow):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.vlc = VlcPlayer(self)
        self.mpv = MpvPlayer(self)

        self.actionStart.triggered.connect(self.onStart)
        self.actionPause.triggered.connect(self.onPause)
        self.actionClose.triggered.connect(self.onStop)

    def _getPlayer(self):
        return getattr(self, videoSettings.VIDEO_PLAYER)

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
