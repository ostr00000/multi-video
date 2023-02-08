from __future__ import annotations

import locale
import logging
from enum import Enum
from functools import partial
from random import randint
from threading import Timer

import mpv
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QApplication
from decorator import decorator

from multi_video.qobjects.settings import videoSettings

logger = logging.getLogger(__name__)


class MpvMouseButton(Enum):
    LEFT = 'MBTN_LEFT'
    RIGHT = 'MBTN_RIGHT'
    MID = 'MBTN_MID'
    DOUBLE = 'MBTN_LEFT_DBL'

    @classmethod
    def getQtButton(cls, button: MpvMouseButton) -> Qt.MouseButton:
        # noinspection PyUnresolvedReferences
        return cls._mapToQt[button]


MpvMouseButton._mapToQt = {
    MpvMouseButton.LEFT: Qt.LeftButton,
    MpvMouseButton.RIGHT: Qt.RightButton,
    MpvMouseButton.MID: Qt.MidButton,
}


@decorator
def ignoreShutdown(fun, *args, **kwargs):
    try:
        fun(*args, **kwargs)
        return True
    except mpv.ShutdownError:
        return False


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
            **{'loop-playlist': 'inf', 'vo': 'x11'}
        )
        self._enableMouseEvent(MpvMouseButton.MID)
        self.setMute()
        self.player.observe_property('filename', self.onFileChanged)

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

        logger.log(level, f'{id(self)}[{component}]: {message.strip()}')

    @ignoreShutdown
    def onFileChanged(self, propertyName, propertyValue, timeDelay=0.3):
        if self.player.filename != propertyValue:
            return
        if not videoSettings.IS_RANDOM_PART_ACTIVE:
            return

        minLength = videoSettings.MINIMAL_LENGTH_TO_ACTIVATE_RANDOM_PART
        duration = self.player.duration
        if duration:
            if duration >= minLength:
                self._setRandomPosition()
                logger.debug(f"[{id(self)}] set random position - new file")
        else:
            Timer(timeDelay, self.onFileChanged,
                  args=(propertyName, propertyValue, timeDelay * 2)).start()
            logger.debug(f"[{id(self)}] no duration property - try again")

    def _setRandomPosition(self):
        if duration := self.player.duration:
            duration = int(duration)
            newDuration = videoSettings.RANDOM_PART_DURATION

            startTime = randint(0, duration - newDuration)
            endTime = startTime + newDuration
            self.player.__setattr__('time-pos', startTime)

            Timer(newDuration, self.onRandomPartEnd, args=(self.player.filename, endTime)).start()

    @ignoreShutdown
    def onRandomPartEnd(self, currentFile, endTime):
        if self.player.filename != currentFile:
            return

        curTime = self.player.__getattr__('time-pos')
        if not curTime:
            return

        if (diff := endTime - curTime) > 0:
            Timer(diff, self.onRandomPartEnd, args=(currentFile, endTime)).start()
            return

        if self.player.__getattr__('playlist-count') == 1:
            self._setRandomPosition()
            logger.debug(f"[{id(self)}] set random position")
        else:
            self.player.playlist_next()
            logger.debug(f"[{id(self)}] play next")

    @ignoreShutdown
    def play(self, filenames: list[str]):
        """For some reason need to wait,
        otherwise deadlock or 'double free or corruption (!prev)' may occur"""
        assert filenames
        with self.player.prepare_and_wait_for_event('file-loaded'):
            isFirst = True
            for fn in filenames:
                if isFirst:
                    self.player.loadfile(fn, 'append-play')
                    isFirst = False
                    continue

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
        self.player.quit(0)
        try:
            self.player.wait_for_shutdown()
        except mpv.ShutdownError:
            pass  # it is what we need

    def closeEvent(self, closeEvent):
        self.stop()
        super().closeEvent(closeEvent)
