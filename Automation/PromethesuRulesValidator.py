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