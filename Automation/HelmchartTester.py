#Helm Chart Tester - Lint, render, and validate Helm charts with custom values
import subprocess
import argparse
import yaml
import tempfile
import os
import json

class HelmTester:
    def __init__(self, chart_path):
        self.chart_path = chart_path
    def lint(self):
        result = subprocess.run(['helm', 'lint', self.chart_path], capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
    def template(self, values_files=None, set_values=None, release_name='test-release'):
        cmd = ['helm', 'template', release_name, self.chart_path]
        for vf in values_files or []:
            cmd.extend(['-f', vf])
        if set_values:
            for key, val in set_values.items():
                cmd.extend(['--set', f'{key}={val}'])
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return result.stderr
    def validate_k8s_manifests(self, rendered_yaml):
        """Use kubeval or kubectl to validate manifests"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(rendered_yaml)
            tmp_file = f.name
        try:
            subprocess.run(['kubectl', 'apply', '--dry-run=client', '-f', tmp_file], capture_output=True, check=True)
            return True, "Valid"
        except subprocess.CalledProcessError as e:
            return False, e.stderr.decode()
        finally:
            os.unlink(tmp_file)
    def run_tests(self, values_files=None, set_values=None):
        lint_ok, lint_out = self.lint()
        if not lint_ok:
            return {'success': False, 'step': 'lint', 'error': lint_out}
        rendered = self.template(values_files, set_values)
        if not rendered:
            return {'success': False, 'step': 'template', 'error': 'Empty output'}
        # Try to split into multiple YAML docs and validate each
        docs = [d for d in rendered.split('---') if d.strip()]
        for doc in docs:
            valid, err = self.validate_k8s_manifests(doc)
            if not valid:
                return {'success': False, 'step': 'validate', 'error': err}
        return {'success': True, 'manifests_count': len(docs)}