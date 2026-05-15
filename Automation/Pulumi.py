import subprocess
import argparse
import sys
import json
from pathlib import Path
 class PulumiManager:
    def __init__(self, stack_name, work_dir='.'):
        self.stack_name = stack_name
        self.work_dir = Path(work_dir)

    def run_cmd(self, cmd):
        full_cmd = ['pulumi', '--cwd', str(self.work_dir)] + cmd
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
