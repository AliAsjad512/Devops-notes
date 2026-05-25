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
    def output(self, output_name=None):
        cmd = ['terraform', 'output', '-json']
        result = subprocess.run(cmd, cwd=self.working_dir, capture_output=True, text=True)
        if result.returncode == 0:
            outputs = json.loads(result.stdout)
            if output_name:
                print(outputs.get(output_name, {}).get('value', 'Not found'))
            else:
                print(json.dumps(outputs, indent=2))
        return result.returncode
    def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default='.', help='Terraform working directory')
    parser.add_argument('--action', choices=['plan', 'apply', 'destroy', 'output'], required=True)
    parser.add_argument('--var', nargs='*', help='Variable assignments (key=value)')
    parser.add_argument('--output-name', help='Specific output name')
    args = parser.parse_args()

    vars_dict = {}
    if args.var:
        for item in args.var:
            key, val = item.split('=', 1)
            vars_dict[key] = val

    tf = TerraformWrapper(args.dir)
    if args.action == 'plan':
        rc = tf.plan(vars_dict)
    elif args.action == 'apply':
        rc = tf.apply(vars_dict)
    elif args.action == 'destroy':
        rc = tf.destroy(vars_dict)
    else:
        rc = tf.output(args.output_name)

    sys.exit(rc)

if __name__ == '__main__':
    main()