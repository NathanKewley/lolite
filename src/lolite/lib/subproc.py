import subprocess
import sys

from lolite.lib.logger import Logger as logger

class Subproc():

    def __init__(self):
        self.logger = logger.get_logger()
        self.logger.propagate = False

    def run_command(self, command):
        result = subprocess.run(command.split(' '), capture_output=True, check=False)
        if result.stdout is not False:
            if type(result.stdout) == bytes:
                return result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
            else:
                return result.stdout + result.stderr
        else:
            return result.stderr
