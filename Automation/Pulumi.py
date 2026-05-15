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
    def preview(self, diff=True):
        cmd = ['preview', '--stack', self.stack_name]
        if not diff:
            cmd.append('--diff='
        returncode, out, err = self.run_cmd(cmd)
        if returncode == 0:
            print(out)
        else:
            print(f"Preview failed: {err}", file=sys.stderr)
        return returncode
     def up(self, yes=True):
        cmd = ['up', '--stack', self.stack_name]
        if yes:
            cmd.append('--yes')
        returncode, out, err = self.run_cmd(cmd)
        if returncode == 0:
            print("✅ Deployment succeeded")
            # Extract outputs
            self.show_outputs()
        else:
            print(f"Deployment failed: {err}", file=sys.stderr)
        return returncode
