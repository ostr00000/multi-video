import logging
from subprocess import Popen, PIPE
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import QEventLoop, QTimer

from const import SLEEP_TIME
from qobjects.time_status_bar import changeStatusDec
from qobjects.window_collector import WindowCollector
from util.commands import runCommand
from util.iterator_wrappers import dataChangeIterator, processEventsIterator
from vlc_model import Row
from vlc_window.base import BaseWindow

logger = logging.getLogger(__name__)


class VideoManager(BaseWindow):
    def __init__(self, *args):
        super().__init__(*args)

        self._processes: List[Popen] = []
        self._isStarting = False

    def _connectButtons(self):
        super()._connectButtons()

        self.actionStart.triggered.connect(self.onStart)
        self.actionPause.triggered.connect(self.onPause)
        self.actionClose.triggered.connect(self.onStop)

    @changeStatusDec(msg="Vlc started.")
    def onStart(self):
        if self._isStarting:
            return

        if self._processes:
            self.onPause(isPause=False)
            self.lower()
            return

        self._isStarting = True
        self._runAll()
        self._isStarting = False

    def _runAll(self):
        windowCollector = WindowCollector()
        loop = QEventLoop()

        for row in dataChangeIterator(
                processEventsIterator(self.model),
                self.model, self.model.COL_PID, self.model.COL_WID):  # type: Row

            if not self._isStarting:
                return

            process = self._runProcess(row)
            self._processes.append(process)

            self.show()
            self.raise_()

            QTimer.singleShot(SLEEP_TIME, loop.quit)
            loop.exec()

            row.pid = process.pid
            row.wid = windowCollector.getNewWindowId()

            self.resizeAndMove(row)
            self.onPause(True, process)

        self.raise_()

    @staticmethod
    def resizeAndMove(row: Row):
        commands = []
        for wid in row.wid[:6]:  # unknown order of layer - may shadow qt interface
            commands.append(f'xdotool windowsize {wid} {row.size[0]} {row.size[1]}')
            commands.append(f'xdotool windowmove {wid} {row.position[0]} {row.position[1]}')

        commandsStr = ' && '.join(commands)
        runCommand(commandsStr)

    @staticmethod
    def _runProcess(row: Row):
        files = ' '.join(f"'{f}'" for f in row.files)
        cmd = f'vlc --intf qt --extraintf rc --qt-minimal-view --started-from-file {files}'
        logger.debug(cmd)
        return Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)

    @changeStatusDec(msg="Vlc paused.", failureMsg="Vlc resumed.")
    def onPause(self, isPause, process=None):
        action = b"pause\n" if isPause else b"play\n"
        self._sendCommand(action, process)

        if process is None:
            self.actionPause.setChecked(isPause)
            self._isStarting = False
            return isPause

    @changeStatusDec(msg="Vlc closed.")
    def onStop(self):
        self._isStarting = False
        self.actionPause.setChecked(False)

        self._sendCommand(b'quit\n')
        self._processes = []
        return True

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

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.onStop()
        super().closeEvent(a0)
