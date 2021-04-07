import subprocess
import sys


def run_command(command):
    result = subprocess.call([command], shell=True)
    return result
