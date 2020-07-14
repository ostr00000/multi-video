import locale
import logging
from asyncio import AbstractEventLoop

import mpv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class MpvPlayerWidget(QWidget):

    def __init__(self, parent=None, eventLoop: AbstractEventLoop = None):
        # TODO remove unused argument or use it in case of poor efficiency
        super().__init__(parent)
        self.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.setAttribute(Qt.WA_NativeWindow)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setMpvLocale()
        self.player = mpv.MPV(
            wid=str(int(self.winId())),
            log_handler=self.logHandler,
            loglevel='info',
        )

    @staticmethod
    def setMpvLocale():
        """
        This is necessary since PyQT stomps over the locale settings needed by libmpv.
        This needs to happen after importing PyQT before creating the first mpv.MPV instance.
        """
        locale.setlocale(locale.LC_NUMERIC, 'C')

    @staticmethod
    def logHandler(loglevel: str, component: str, message: str):
        level = logging.getLevelName(loglevel.upper())
        if isinstance(level, str):
            level = logging.DEBUG

        logger.log(level, f'[{component}]: {message}')

    def play(self, filename):
        self.player.play(filename)

    def stop(self):
        self.player.quit()

    def closeEvent(self, closeEvent):
        self.stop()
        super().closeEvent(closeEvent)
