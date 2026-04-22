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
        
    def get_env_config(self, env):
        env_file = self.env_config_dir / f"{env}.yaml"
        if not env_file.exists():
            raise FileNotFoundError(f"Config for env {env} not found")
        env_override = self._load_yaml(env_file)
        # Deep merge: env overrides base
        merged = self._deep_merge(copy.deepcopy(self.base), env_override)
        return merged
    def _deep_merge(self, base, override):
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
