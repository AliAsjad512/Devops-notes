import boto3
import argparse
import json
 class ConfigRuleEvaluator:
    def __init__(self, region='us-east-1'):
        self.config = boto3.client('config', region_name=region)

    def get_compliance_summary(self):
        response = self.config.describe_compliance_by_config_rule()
        summary = []
        for rule in response['ComplianceByConfigRules']:
            summary.append({
                'rule_name': rule['ConfigRuleName'],
                'compliance': rule['Compliance']['ComplianceType']
            })
        return summary