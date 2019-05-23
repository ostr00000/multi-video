from subprocess import Popen, PIPE
from typing import List

from multi_vlc.vlc_model import Row


class ProcessController:

    def __init__(self):
        self._processes: List[Popen] = []
        self.thread = None

    def run(self, row: Row):
        files = ' '.join(row.files)
        process = Popen(f'vlc --intf qt --extraintf rc --started-from-file {files}',
                        shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)
        self._processes.append(process)
        return process.pid

    def update(self):
        self._processes = [p for p in self._processes if p.poll() is not None]

    def setPause(self, isPause: bool):
        self.update()
        action = "pause\n" if isPause else "play\n"
        for process in self._processes:
            process.stdin.write(action)

    def terminate(self):
        for process in self._processes:
            process.terminate()
        self._processes = []
