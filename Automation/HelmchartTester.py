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