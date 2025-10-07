import logging
import shlex
import shutil
import uuid
from functools import cached_property
from pathlib import Path
from subprocess import PIPE, Popen

from PyQt5.QtCore import QEventLoop, QStandardPaths, QTimer

from multi_video import appName
from multi_video.model.row import BaseRow
from multi_video.player.base import BasePlayer
from multi_video.qobjects.settings import videoSettings
from multi_video.utils.commands import runCommand
from multi_video.utils.iterator_wrappers import (
    dataChangeIterator,
    processEventsIterator,
)
from multi_video.utils.window_collector import WindowCollector
from multi_video.window.base import BaseVideoWindow

logger = logging.getLogger(__name__)


class VlcPlayer(BasePlayer):
    def __init__(self, baseWindow: BaseVideoWindow, *args):
        super().__init__(baseWindow, *args)

        self._processes: list[Popen[bytes]] = []
        self._isStarting = False

    def onStart(self):
        if self._isStarting:
            return None

        if self._processes:
            self.onPause(isPause=False)
            self.baseWindow.lower()
            return None

        self._isStarting = True
        self._runAll()
        self._isStarting = False
        return True

    def _runAll(self):
        windowCollector = WindowCollector()
        loop = QEventLoop()

        for row in dataChangeIterator(
            processEventsIterator(iter(self.model)),
            self.model,
            self.model.COL_PID,
            self.model.COL_WID,
        ):
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
            self.onPause(isPause=True, process=process)

        self.baseWindow.raise_()

    @staticmethod
    def resizeAndMove(row: BaseRow):
        commands: list[str] = []
        for wid in row.wid[:6]:  # unknown order of layer - may shadow qt interface
            cmd = [
                'xdotool',
                'windowsize',
                str(wid),
                str(row.size[0]),
                str(row.size[1]),
            ]
            commands.append(shlex.join(cmd))

            cmd = [
                'xdotool',
                'windowmove',
                str(wid),
                str(row.position[0]),
                str(row.position[1]),
            ]
            commands.append(shlex.join(cmd))

        runCommand(' && '.join(commands))

    def _runProcess(self, row: BaseRow) -> Popen[bytes]:
        cmd = [
            'vlc',
            '--verbose',
            '3',
            '--intf',
            'qt',
            '--extraintf',
            'rc',
            '--qt-minimal-view',
            '--started-from-file',
            *row.getFiles(),
        ]
        logger.debug(cmd)

        logFile = self.getLogFile(row)
        return Popen(
            cmd,
            stderr=logFile,
            stdout=logFile,
            stdin=PIPE,
        )

    def getLogFile(self, row: BaseRow):
        return (self.logDirPath / f'{row.position}_{uuid.uuid4()}').open('w')

    @cached_property
    def logDirPath(self) -> Path:
        sps = QStandardPaths.standardLocations(QStandardPaths.TempLocation)
        logPath = Path(sps[0])
        dirPath = logPath / appName
        shutil.rmtree(dirPath, ignore_errors=True)
        dirPath.mkdir(parents=True, exist_ok=True)
        return dirPath

    def onPause(self, *, isPause: bool, process: Popen[bytes] | None = None):
        action = b"pause\n" if isPause else b"play\n"
        self._sendCommand(action, process)

        if process is None:
            self.baseWindow.actionPause.setChecked(isPause)
            self._isStarting = False
            return isPause
        return None

    def onStop(self):
        self._isStarting = False
        self.baseWindow.actionPause.setChecked(False)

        oldProcesses = self._sendCommand(b'quit\n')
        self._killProcesses(oldProcesses)
        self._processes: list[Popen[bytes]] = []
        return True

    def _sendCommand(self, command: bytes, process: Popen[bytes] | None = None):
        processes = [process] if process else self._processes
        valid: list[Popen[bytes]] = []
        for p in processes:
            if p.stdin is None:
                continue
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
    def _killProcesses(processes: list[Popen[bytes]]):
        if any(p.poll() is None for p in processes):
            loop = QEventLoop()
            QTimer.singleShot(videoSettings.VLC_SLEEP_TIME_LLmsJJ, loop.quit)
            loop.processEvents()

        for p in processes:
            if p.poll():
                continue
            logger.debug(f'Killing process {p.pid}')
            p.kill()
