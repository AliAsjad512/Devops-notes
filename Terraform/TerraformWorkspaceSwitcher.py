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
    def delete_workspace(self, name):
        if name == 'default':
            print("❌ Cannot delete default workspace")
            return
        rc, out, err = self.run_cmd(['terraform', 'workspace', 'delete', name])
        if rc == 0:
            print(f"🗑️ Workspace '{name}' deleted")
        else:
            print(f"❌ {err}")
    def current_workspace(self):
        workspaces = self.list_workspaces()
        for line in workspaces:
            pass  # Not straightforward; use `terraform workspace show`
        rc, out, err = self.run_cmd(['terraform', 'workspace', 'show'])
        return out.strip()
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Terraform Workspace Switcher')
    parser.add_argument('--dir', default='.')
    parser.add_argument('--action', choices=['list', 'create', 'select', 'delete', 'current'], required=True)
    parser.add_argument('--name', help='Workspace name')
    args = parser.parse_args()

    ws = TerraformWorkspace(args.dir)
    if args.action == 'list':
        workspaces = ws.list_workspaces()
        current = ws.current_workspace()
        for w in workspaces:
            marker = '*' if w == current else ' '
            print(f"{marker} {w}")
    elif args.action == 'create':
        ws.create_workspace(args.name)
    elif args.action == 'select':
        ws.select_workspace(args.name)
    elif args.action == 'delete':
        ws.delete_workspace(args.name)
    elif args.action == 'current':
        print(ws.current_workspace())
