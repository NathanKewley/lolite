import subprocess
import sys
from lib.logger import Logger as logger

logger = logger.get_logger()


def run_command(command):
    result = subprocess.run(command.split(' '), capture_output=True, check=True)
    if result.stdout is not False:
        if type(result.stdout) == bytes:
            return result.stdout.decode("utf-8")
        else:
            return result.stdout
    else:
        logger.error(str(result.stderr))
