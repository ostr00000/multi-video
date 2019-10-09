import logging
from subprocess import Popen, PIPE
from typing import List

from multi_vlc.vlc_model import Row

logger = logging.getLogger(__name__)


class ProcessController:

    def __init__(self):
        self._processes: List[Popen] = []
        self.thread = None

    def run(self, row: Row):
        files = ' '.join(f"'{f}'" for f in row.files)
        cmd = f'vlc --intf qt --extraintf rc --started-from-file {files}'
        logger.debug(cmd)
        process = Popen(cmd, shell=True,
                        stderr=PIPE,
                        stdout=PIPE,
                        stdin=PIPE)
        self._processes.append(process)
        return process.pid

    def sendCommand(self, command, process=None):
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

    def setPause(self, isPause: bool, pid=None):
        action = b"pause\n" if isPause else b"play\n"
        process = next(p for p in self._processes if p.pid == pid) if pid else None
        self.sendCommand(action, process)

    def terminate(self):
        self.sendCommand(b'quit\n')
        self._processes = []

    def isRunning(self):
        return bool(self._processes)
