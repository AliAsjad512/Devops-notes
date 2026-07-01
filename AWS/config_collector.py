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
    
     def print_report(self):
        report = self.generate_report()
        print("AWS Config Compliance Report:")
        print("-" * 50)
        for r in report:
            status = "✅" if r['compliance'] == 'COMPLIANT' else "❌"
            print(f"{status} {r['name']}: {r['compliance']}")

            if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', default='us-east-1')
    args = parser.parse_args()

    collector = ConfigCollector(args.region)
    collector.print_report()