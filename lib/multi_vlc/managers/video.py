import logging
import os
import shutil
import uuid
from subprocess import Popen, PIPE
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import QEventLoop, QTimer, QStandardPaths
from boltons.cacheutils import cachedproperty

from multi_vlc import appName
from multi_vlc.const import SLEEP_TIME
from multi_vlc.qobjects.time_status_bar import changeStatusDec
from multi_vlc.qobjects.window_collector import WindowCollector
from multi_vlc.utils.commands import runCommand
from multi_vlc.utils.iterator_wrappers import dataChangeIterator, processEventsIterator
from multi_vlc.vlc_model import Row
from multi_vlc.vlc_window.base import BaseWindow

logger = logging.getLogger(__name__)


class VideoManager(BaseWindow):
    def __init__(self, *args):
        super().__init__(*args)

        self._processes: List[Popen] = []
        self._isStarting = False

    def __post_init__(self):
        super().__post_init__()

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

    def _runProcess(self, row: Row) -> Popen:
        files = ' '.join(f"'{f}'" for f in row.files)
        cmd = f'vlc --verbose 3 --intf qt --extraintf rc ' \
              f'--qt-minimal-view --started-from-file {files}'
        logger.debug(cmd)

        logFile = self.getLogFile(row)
        return Popen(cmd, shell=True, stderr=logFile, stdout=logFile, stdin=PIPE)

    def getLogFile(self, row: Row):
        filePath = os.path.join(self.logDir, f'{row.position}_{uuid.uuid4()}')
        logFile = open(filePath, 'w')
        return logFile

    @cachedproperty
    def logDir(self):
        dirPath = os.path.join(
            QStandardPaths.standardLocations(QStandardPaths.TempLocation)[0],
            appName)
        shutil.rmtree(dirPath, ignore_errors=True)
        os.makedirs(dirPath, exist_ok=True)
        return dirPath

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

        oldProcesses = self._sendCommand(b'quit\n')
        self._killProcesses(oldProcesses)
        self._processes = []
        return True

    def _sendCommand(self, command, process: Popen = None):
        processes = [process] if process else self._processes
        valid: List[Popen] = []
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

        return processes

    @staticmethod
    def _killProcesses(processes: List[Popen]):
        if any(p.poll() is None for p in processes):
            loop = QEventLoop()
            QTimer.singleShot(SLEEP_TIME, loop.quit)
            loop.processEvents()

        for p in processes:
            if p.poll():
                continue
            logger.debug(f'Killing process {p.pid}')
            p.kill()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.onStop()
        super().closeEvent(a0)
