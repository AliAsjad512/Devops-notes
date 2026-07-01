import boto3
import argparse
import json

class ConfigCollector:
    def __init__(self, region='us-east-1'):
        self.config = boto3.client('config', region_name=region)

     def get_all_rules(self):
        rules = self.config.describe_config_rules()['ConfigRules']
        return rules
     def get_compliance(self, rule_name):
        response = self.config.describe_compliance_by_config_rule(ConfigRuleNames=[rule_name])
        return response['ComplianceByConfigRules'][0]['Compliance']['ComplianceType']
    
    def generate_report(self):
        rules = self.get_all_rules()
        report = []
        for rule in rules:
            name = rule['ConfigRuleName']
            compliance = self.get_compliance(name)
            report.append({
                'name': name,
                'compliance': compliance,
                'source': rule['Source']['Owner']
            })
        return report