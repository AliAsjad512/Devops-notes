import boto3
import argparse
import json
 class ConfigRuleEvaluator:
    def __init__(self, region='us-east-1'):
        self.config = boto3.client('config', region_name=region)