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
    def list_workspaces(self):
        rc, out, err = self.run_cmd(['terraform', 'workspace', 'list'])
        if rc != 0:
            print(f"Error: {err}")
            return []
        workspaces = []
        for line in out.split('\n'):
            line = line.strip()
            if line:
                workspaces.append(line.lstrip('* ').strip())
        return workspaces
    def create_workspace(self, name):
        rc, out, err = self.run_cmd(['terraform', 'workspace', 'new', name])
        if rc == 0:
            print(f"✅ Workspace '{name}' created")
        else:
            print(f"❌ {err}")
    def select_workspace(self, name):
        rc, out, err = self.run_cmd(['terraform', 'workspace', 'select', name])
        if rc == 0:
            print(f"✅ Switched to workspace '{name}'")
        else:
            print(f"❌ {err}")