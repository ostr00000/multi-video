from subprocess import Popen, PIPE

from multi_vlc.vlc_model import Row


class ProcessController:

    def __init__(self):
        self._processes = []

    def run(self, row: Row):
        process = Popen(f'vlc --intf qt --extraintf rc', shell=True,
                        stderr=PIPE, stdout=PIPE, stdin=PIPE)
        output, stderr = process.communicate()  # TODO

    def setPause(self, isPause: bool):
        pass

    def terminate(self):
        pass
