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
    def diff_envs(self, env1, env2):
        cfg1 = self.get_env_config(env1)
        cfg2 = self.get_env_config(env2)
        diff = DeepDiff(cfg1, cfg2, ignore_order=True)
        return diff.to_dict()
    def validate(self, env, schema_path=None):
        """Validate config against JSON schema"""
        if schema_path:
            import jsonschema
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            config = self.get_env_config(env)
            try:
                jsonschema.validate(config, schema)
                print(f"✅ Config for {env} is valid")
            except jsonschema.ValidationError as e:
                print(f"❌ Config invalid: {e}")
                return False
        return True
    def export(self, env, output_format='json'):
        config = self.get_env_config(env)
        if output_format == 'json':
            print(json.dumps(config, indent=2))
        else:
            print(yaml.dump(config))

    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multi-Environment Config Manager')
    parser.add_argument('--base', required=True, help='Base config YAML')
    parser.add_argument('--env-dir', required=True, help='Environment overrides directory')
    parser.add_argument('--env', required=True, help='Environment name')
    parser.add_argument('--action', choices=['show', 'diff', 'validate', 'export'], default='show')
    parser.add_argument('--diff-with', help='Second environment for diff')
    parser.add_argument('--schema', help='JSON schema for validation')
    parser.add_argument('--format', choices=['json', 'yaml'], default='json')
    args = parser.parse_args()

    mgr = ConfigManager(args.base, args.env_dir)
    if args.action == 'show':
        config = mgr.get_env_config(args.env)
        print(yaml.dump(config))
    elif args.action == 'diff':
        if not args.diff_with:
            print("❌ --diff-with required for diff action")
        else:
            diff = mgr.diff_envs(args.env, args.diff_with)
            if diff:
                print(json.dumps(diff, indent=2))
            else:
                print("Configs are identical")
    elif args.action == 'validate':
        mgr.validate(args.env, args.schema)
    elif args.action == 'export':
        mgr.export(args.env, args.format)