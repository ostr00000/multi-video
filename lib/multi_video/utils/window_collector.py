import logging

from PyQt5.QtCore import QThread

from multi_video.qobjects.settings import videoSettings
from multi_video.utils.commands import runCommand

logger = logging.getLogger(__name__)


class WindowCollector:
    def __init__(self):
        self.allWid = set(self.getWid())

    def getNewWindowId(self):
        try:
            newerWid = set(self.getWid())
        except ValueError:
            QThread.msleep(videoSettings.VLC_SLEEP_TIME_LLmsJJ)
            try:
                newerWid = set(self.getWid())
            except ValueError as er:
                logger.error(er)
                return []

        ret = list(newerWid - self.allWid)
        self.allWid = newerWid
        return ret

    @staticmethod
    def getWid():
        output = runCommand('xdotool search vlc')
        if not output:
            logger.warning("xdotool return empty string")
        output = [int(wid) for wid in output.split('\n')]
        return output
