import json
import yaml
import argparse
import os
import copy
from pathlib import Path
from deepdiff import DeepDiff

class ConfigManager:
    def __init__(self, base_config_path, env_config_dir):
        self.base_config_path = Path(base_config_path)
        self.env_config_dir = Path(env_config_dir)
        self.base = self._load_yaml(base_config_path)
    def _load_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)
