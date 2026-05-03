import os
import sys
import argparse
import re

class EnvValidator:
    def __init__(self, required_vars=None, patterns=None):
        self.required_vars = required_vars or []
        self.patterns = patterns or {}
    def add_required(self, var_name):
        self.required_vars.append(var_name)
    def add_pattern(self, var_name, regex):
        self.patterns[var_name] = regex
    def validate(self):
        errors = []
        for var in self.required_vars:
            if var not in os.environ or not os.environ[var]:
                errors.append(f"Missing required env var: {var}")
        for var, pattern in self.patterns.items():
            value = os.environ.get(var, '')
            if not re.match(pattern, value):
                errors.append(f"Env var {var}='{value}' does not match required pattern: {pattern}")
        return errors
    def validate_from_file(self, config_file):
        import yaml
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        self.required_vars = config.get('required', [])
        self.patterns = config.get('patterns', {})
        return self.validate()



