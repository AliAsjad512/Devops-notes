import subprocess
import argparse
import sys
import os
import json
class TerraformWrapper:
    def __init__(self, working_dir='.'):
        self.working_dir = working_dir
    def run(self, command, vars=None):
        cmd = ['terraform', command]
        if vars:
            for k, v in vars.items():
                cmd.extend(['-var', f'{k}={v}'])
        if command == 'apply':
            cmd.append('-auto-approve')
        result = subprocess.run(cmd, cwd=self.working_dir, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode
    def plan(self, vars=None):
        return self.run('plan', vars)

    def apply(self, vars=None):
        return self.run('apply', vars)

    def destroy(self, vars=None):
        return self.run('destroy', vars)