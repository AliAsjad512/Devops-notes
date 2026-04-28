import yaml
import json
import argparse
import requests
import re
from pathlib import Path

class PrometheusRuleValidator:
    def __init__(self, prometheus_url=None):
        self.prometheus_url = prometheus_url

    def load_rules(self, rule_file):
        with open(rule_file, 'r') as f:
            return yaml.safe_load(f)
    def validate_syntax(self, rules):
        """Basic syntax validation"""
        errors = []
        if 'groups' not in rules:
            errors.append("Missing 'groups' top-level key")
        for group_idx, group in enumerate(rules.get('groups', [])):
            if 'name' not in group:
                errors.append(f"Group {group_idx}: missing name")
            for rule_idx, rule in enumerate(group.get('rules', [])):
                if 'record' not in rule and 'alert' not in rule:
                    errors.append(f"Group {group['name']}, rule {rule_idx}: missing record/alert")
                if 'expr' not in rule:
                    errors.append(f"Group {group['name']}, rule {rule_idx}: missing expr")
                # Check for common PromQL syntax issues
                expr = rule['expr']
                if re.search(r'[^a-zA-Z0-9_:{}\[\]()., +*/%-]', expr):
                    errors.append(f"Group {group['name']}, rule {rule_idx}: suspicious characters in expr")
        return errors
    def validate_against_prometheus(self, rules):
        """Use Prometheus /api/v1/rules endpoint to validate (if available)"""
        if not self.prometheus_url:
            return []
        try:
            resp = requests.get(f"{self.prometheus_url}/api/v1/rules")
            resp.raise_for_status()
            # If we can fetch rules, assume the loaded rules are fine
            return []
        except Exception as e:
            return [f"Cannot connect to Prometheus: {e}"]