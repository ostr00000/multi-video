import logging
from subprocess import PIPE, Popen

logger = logging.getLogger(__name__)


def runCommand(command: str) -> str:
    logger.debug(f"Executing: '{command}'")

    process = Popen(
        [
            '/usr/bin/bash',
            '-c',
            command,
        ],
        text=True,
        stdout=PIPE,
        stderr=PIPE,
    )

    stdout = process.communicate()[0]
    return stdout.rstrip()
