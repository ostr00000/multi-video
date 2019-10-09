import logging
import re
from subprocess import Popen, PIPE
from typing import Set

from multi_vlc.vlc_model import Row

logger = logging.getLogger(__name__)
vlcFileArgPattern = re.compile(r'.*vlc.*--started-from-file( \'?.*\.\w+\'?)+')
filesPattern = re.compile(r'\'?(.*?\.\w+)\'?')


def runCommand(command) -> str:
    logger.debug(f"Executing: '{command}'")
    process = Popen(command, stdout=PIPE, shell=True, stderr=PIPE)
    stdout = process.communicate()[0]
    result = stdout.decode('utf-8').rstrip()
    return result


def getRunningVlc() -> Set[str]:
    output = runCommand('ps -eo pid,command | grep vlc')
    result = set()
    for line in output.split('\n'):
        pid, command = line.split(maxsplit=1)
        match = vlcFileArgPattern.match(command)
        if match:
            filesStr = match.group(1).lstrip()
            files = filesPattern.split(filesStr)
            files = [file.lstrip() for file in filter(None, files)]
            for f in files:
                result.add(f)

    return result


def getWid():
    output = runCommand('xdotool search vlc')
    if not output:
        logger.warning("xdotool return empty string")
    output = [int(wid) for wid in output.split('\n')]
    return output


def resizeAndMove(row: Row):
    commands = []
    for wid in row.wid:
        commands.append(f'xdotool windowsize {wid} {row.size[0]} {row.size[1]}')
        commands.append(f'xdotool windowmove {wid} {row.position[0]} {row.position[1]}')

    commandsStr = ' && '.join(commands)
    runCommand(commandsStr)
