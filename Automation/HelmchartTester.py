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