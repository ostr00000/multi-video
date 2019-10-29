import logging
from subprocess import Popen, PIPE
from typing import TYPE_CHECKING, List

from PyQt5.QtCore import QObject, pyqtSlot, QThread
from commands import getWid, resizeAndMove
from const import SLEEP_TIME
from decoators import changeStatusDec, SlotDecorator, processEventsIterator, dataChangeIterator
from multi_vlc.vlc_model import Row

if TYPE_CHECKING:
    from vlc_window import VlcWindow

logger = logging.getLogger(__name__)


class WindowCollector:
    def __init__(self):
        self.allWid = set(getWid())

    def getNewWindowId(self):
        try:
            newerWid = set(getWid())
        except ValueError:
            QThread.msleep(SLEEP_TIME)
            try:
                newerWid = set(getWid())
            except ValueError as er:
                logger.error(er)
                return []

        ret = list(newerWid - self.allWid)
        self.allWid = newerWid
        return ret


class ProcessController(QObject, metaclass=SlotDecorator):

    def __init__(self, parent: 'VlcWindow'):
        super().__init__(parent)
        self._processes: List[Popen] = []
        self._isStarting = False

    @pyqtSlot()
    @changeStatusDec(msg="Vlc started.")
    def onStart(self):
        if self._isStarting:
            return

        if self._processes:
            self.onPause(isPause=False)
            return

        self._isStarting = True
        self._runAll()
        self._isStarting = False

    def _runAll(self):
        p: 'VlcWindow' = self.parent()
        windowCollector = WindowCollector()

        for row in dataChangeIterator(processEventsIterator(p.model), p.model,
                                      p.model.COL_PID, p.model.COL_WID):  # type: Row
            popen = self._runProcess(row)
            self._processes.append(popen)
            QThread.msleep(SLEEP_TIME)
            self.onPause(True, popen)

            row.pid = popen.pid
            row.wid = windowCollector.getNewWindowId()

            resizeAndMove(row)

        p.raise_()

    @pyqtSlot(bool)
    @changeStatusDec(msg="Vlc paused.", failureMsg="Vlc resumed.")
    def onPause(self, isPause, process=None):
        action = b"pause\n" if isPause else b"play\n"
        self._sendCommand(action, process)

        if process is None:
            self.parent().actionPause.setChecked(isPause)
            return isPause

    @pyqtSlot()
    @changeStatusDec(msg="Vlc closed.")
    def onStop(self):
        self._isStarting = False
        self.parent().actionPause.setChecked(False)

        self._sendCommand(b'quit\n')
        self._processes = []
        return True

    @staticmethod
    def _runProcess(row: Row):
        files = ' '.join(f"'{f}'" for f in row.files)
        # --qt-minimal-view  not work as expected
        cmd = f'vlc --intf qt --extraintf rc --started-from-file {files}'
        logger.debug(cmd)
        return Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)

    def _sendCommand(self, command, process=None):
        processes = [process] if process else self._processes
        valid = []
        for p in processes:
            try:
                logger.debug(f"Sending: {command} for {p.pid}")
                p.stdin.write(command)
                p.stdin.flush()
            except BrokenPipeError:
                pass
            else:
                valid.append(p)

        if not process:
            self._processes = valid
