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

