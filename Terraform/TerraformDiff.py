import subprocess
import json
import argparse
import requests
from deepdiff import DeepDiff
from pathlib import Path

class TfStateDiff:
    def __init__(self, state_path):
        self.state_path = Path(state_path)
    def load_state(self):
        with open(self.state_path, 'r') as f:
            return json.load(f)
    def extract_resources(self, state):
        resources = {}
        for resource in state.get('resources', []):
            if resource.get('mode') == 'managed':
                for instance in resource.get('instances', []):
                    key = f"{resource['type']}.{resource['name']}"
                    resources[key] = {
                        'type': resource['type'],
                        'name': resource['name'],
                        'attributes': instance.get('attributes', {})
                    }
        return resources
    def diff_with(self, other_state_path):
        state1 = self.load_state()
        state2 = TfStateDiff(other_state_path).load_state()
        res1 = self.extract_resources(state1)
        res2 = self.extract_resources(state2)
        diff = DeepDiff(res1, res2, ignore_order=True, exclude_regex_paths=r".*\.id$")
        return diff

