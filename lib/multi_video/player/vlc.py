import logging
import os
import shutil
import uuid
from subprocess import Popen, PIPE
from typing import List

from PyQt5.QtCore import QEventLoop, QTimer, QStandardPaths
from boltons.cacheutils import cachedproperty

from multi_video import appName
from multi_video.model.row import BaseRow
from multi_video.player.base import BasePlayer
from multi_video.qobjects.settings import videoSettings
from multi_video.utils.commands import runCommand
from multi_video.utils.iterator_wrappers import dataChangeIterator, processEventsIterator
from multi_video.utils.window_collector import WindowCollector
from multi_video.window.base import BaseVideoWindow

logger = logging.getLogger(__name__)


class VlcPlayer(BasePlayer):
    def __init__(self, baseWindow: BaseVideoWindow, *args):
        super().__init__(baseWindow, *args)

        self._processes: List[Popen] = []
        self._isStarting = False

    def onStart(self):
        if self._isStarting:
            return

        if self._processes:
            self.onPause(isPause=False)
            self.baseWindow.lower()
            return

        self._isStarting = True
        self._runAll()
        self._isStarting = False
        return True

    def _runAll(self):
        windowCollector = WindowCollector()
        loop = QEventLoop()

        for row in dataChangeIterator(
                processEventsIterator(self.model),
                self.model, self.model.COL_PID, self.model.COL_WID):  # type: BaseRow

            if not self._isStarting:
                return

            process = self._runProcess(row)
            self._processes.append(process)

            self.baseWindow.show()
            self.baseWindow.raise_()

            QTimer.singleShot(videoSettings.VLC_SLEEP_TIME_LLmsJJ, loop.quit)
            loop.exec()

            row.pid = process.pid
            row.wid = windowCollector.getNewWindowId()

            self.resizeAndMove(row)
            self.onPause(True, process)

        self.baseWindow.raise_()

    @staticmethod
    def resizeAndMove(row: BaseRow):
        commands = []
        for wid in row.wid[:6]:  # unknown order of layer - may shadow qt interface
            commands.append(f'xdotool windowsize {wid} {row.size[0]} {row.size[1]}')
            commands.append(f'xdotool windowmove {wid} {row.position[0]} {row.position[1]}')

        commandsStr = ' && '.join(commands)
        runCommand(commandsStr)

    def _runProcess(self, row: BaseRow) -> Popen:
        files = ' '.join(f"'{f}'" for f in row.getFiles())
        cmd = f'vlc --verbose 3 --intf qt --extraintf rc ' \
              f'--qt-minimal-view --started-from-file {files}'
        logger.debug(cmd)

        logFile = self.getLogFile(row)
        return Popen(cmd, shell=True, stderr=logFile, stdout=logFile, stdin=PIPE)

    def getLogFile(self, row: BaseRow):
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

    def onPause(self, isPause, process=None):
        action = b"pause\n" if isPause else b"play\n"
        self._sendCommand(action, process)

        if process is None:
            self.baseWindow.actionPause.setChecked(isPause)
            self._isStarting = False
            return isPause

    def onStop(self):
        self._isStarting = False
        self.baseWindow.actionPause.setChecked(False)

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
            QTimer.singleShot(videoSettings.VLC_SLEEP_TIME_LLmsJJ, loop.quit)
            loop.processEvents()

        for p in processes:
            if p.poll():
                continue
            logger.debug(f'Killing process {p.pid}')
            p.kill()
