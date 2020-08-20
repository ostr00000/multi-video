from __future__ import annotations

import locale
import logging
from enum import Enum
from functools import partial
from typing import List

import mpv
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QApplication

logger = logging.getLogger(__name__)


class MpvMouseButton(Enum):
    LEFT = 'MBTN_LEFT'
    RIGHT = 'MBTN_RIGHT'
    MID = 'MBTN_MID'
    DOUBLE = 'MBTN_LEFT_DBL'

    @classmethod
    def getQtButton(cls, button: MpvMouseButton) -> Qt.MouseButton:
        return cls._mapToQt[button]


MpvMouseButton._mapToQt = {
    MpvMouseButton.LEFT: Qt.LeftButton,
    MpvMouseButton.RIGHT: Qt.RightButton,
    MpvMouseButton.MID: Qt.MidButton,
}


class MpvPlayerWidget(QWidget):
    class LogLevel:
        DEBUG = 'debug'
        INFO = 'info'
        NO = 'no'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.setAttribute(Qt.WA_NativeWindow)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setMpvLocale()
        logger.debug(f"Creating media player {id(self)}")

        self.player = mpv.MPV(
            wid=str(int(self.winId())),
            log_handler=self.logHandler,
            loglevel=self.LogLevel.INFO,
            **{'loop-playlist': 'inf'}
        )
        self._enableMouseEvent(MpvMouseButton.MID)
        self.setMute()

    def _enableMouseEvent(self, mouseButton: MpvMouseButton):
        callback = partial(self._mousePress, mouseButton)
        self.player.on_key_press(mouseButton.value)(callback)

    def _mousePress(self, mouseButton: MpvMouseButton):
        qtButton = MpvMouseButton.getQtButton(mouseButton)
        event = QMouseEvent(
            QMouseEvent.MouseButtonPress, QPointF(),
            qtButton, qtButton, Qt.NoModifier)
        QApplication.sendEvent(self, event)

    @staticmethod
    def setMpvLocale():
        """
        This is necessary since PyQT stomps over the locale settings needed by libmpv.
        This needs to happen after importing PyQT before creating the first mpv.MPV instance.
        """
        locale.setlocale(locale.LC_NUMERIC, 'C')

    def logHandler(self, loglevel: str, component: str, message: str):
        level = logging.getLevelName(loglevel.upper())
        if isinstance(level, str):
            level = logging.DEBUG

        logger.log(level, f'{id(self)}[{component}]: {message}')

    def play(self, filenames: List[str]):
        """For some reason need to wait,
        otherwise deadlock or 'double free or corruption (!prev)' may occur"""
        assert filenames
        try:
            with self.player.prepare_and_wait_for_event('file-loaded'):
                self._play(filenames)
            return True
        except mpv.ShutdownError:
            return False

    def _play(self, filenames):
        isFirst = True
        for fn in filenames:
            if isFirst:
                self.player.loadfile(fn, 'append-play')
                isFirst = False

            self.player.playlist_append(fn)

    def setPause(self, isPause: bool = True, change=False):
        if change:
            self.player.cycle('pause')
        else:
            self.player.pause = isPause

    def setMute(self, isMute: bool = True, change=False):
        if change:
            self.player.cycle('mute')
        else:
            self.player.mute = isMute

    def stop(self):
        self.player.quit()
        try:
            self.player.wait_for_shutdown()
        except mpv.ShutdownError:
            pass  # it is what we need

    def closeEvent(self, closeEvent):
        self.stop()
        super().closeEvent(closeEvent)
