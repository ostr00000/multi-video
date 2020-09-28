import logging
from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)


def runCommand(command) -> str:
    logger.debug(f"Executing: '{command}'")
    process = Popen(command, stdout=PIPE, shell=True, stderr=PIPE)
    stdout = process.communicate()[0]
    result = stdout.decode('utf-8').rstrip()
    return result
