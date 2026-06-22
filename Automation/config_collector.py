import boto3
import argparse
import json

class ConfigCollector:
    def __init__(self, region='us-east-1'):
        self.config = boto3.client('config', region_name=region)
    
    def get_all_rules(self):
        rules = self.config.describe_config_rules()['ConfigRules']
        return rules