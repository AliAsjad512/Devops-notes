import subprocess
import argparse
import sys
import re
class TerraformWorkspace:
    def __init__(self, tf_dir='.'):
        self.tf_dir = tf_dir
    def run_cmd(self, cmd):
        result = subprocess.run(cmd, cwd=self.tf_dir, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
