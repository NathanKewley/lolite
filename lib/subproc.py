import subprocess
import sys


def run_command(command):
    result = subprocess.getoutput([command])
    return result
