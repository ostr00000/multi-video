import re
from subprocess import Popen, PIPE
from typing import Tuple, List

from multi_vlc.vlc_model import Row

vlcFileArgPattern = re.compile('.*vlc.*--started-from-file( .*\.\w+)+')
filesPattern = re.compile('(.*?\.\w+)')


def runCommand(command) -> str:
    process = Popen(command, stdout=PIPE, shell=True, stderr=PIPE)
    stdout = process.communicate()[0]
    result = stdout.decode('utf-8').rstrip()
    return result


def getRunningVlc() -> List[Tuple[int, List[str]]]:
    output = runCommand('ps -eo pid,command | grep vlc')
    result = []
    for line in output.split('\n'):
        pid, command = line.split(maxsplit=1)
        pid = int(pid)
        match = vlcFileArgPattern.match(command)
        if match:
            filesStr = match.group(1).lstrip()
            files = filesPattern.split(filesStr)
            files = [file.lstrip() for file in filter(None, files)]
            result.append((pid, files))

    return result


def getWidFromPid(pid: int):
    output = runCommand(f'xdotool search --pid {pid}')
    output = [int(wid) for wid in output.split('\n')]
    return output


def resizeAndMove(row: Row):
    for wid in row.wid:
        runCommand(f'xdotool windowsize {wid} {row.size[0]} {row.size[1]}')
        runCommand(f'xdotool windowmove {wid} {row.position[0]} {row.position[1]}')
