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
    
     def get_non_compliant_resources(self, rule_name):
        response = self.config.get_compliance_details_by_config_rule(
            ConfigRuleName=rule_name,
            ComplianceTypes=['NON_COMPLIANT']
        )
        resources = []
        for evaluation in response.get('EvaluationResults', []):
            resources.append({
                'resource_id': evaluation['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId'],
                'resource_type': evaluation['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceType'],
                'annotation': evaluation.get('Annotation', '')
            })
        return resources
    def evaluate_custom_rule(self, rule_name, resource_type, resource_id, compliance_type):
        """Manually evaluate a resource against a custom rule"""
        response = self.config.put_evaluations(
            Evaluations=[{
                'ComplianceResourceType': resource_type,
                'ComplianceResourceId': resource_id,
                'ComplianceType': compliance_type,
                'Annotation': f"Manual evaluation at {datetime.utcnow()}"
            }],
            ResultToken='manual'
        )
        return response['FailedEvaluations'] == []
    
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AWS Config Rule Evaluator')
    parser.add_argument('--region', default='us-east-1')
    parser.add_argument('--action', choices=['summary', 'details'], default='summary')
    parser.add_argument('--rule', help='Config rule name for details')
    args = parser.parse_args()

    evaluator = ConfigRuleEvaluator(args.region)
    if args.action == 'summary':
        summary = evaluator.get_compliance_summary()
        print("Config rule compliance summary:")
        for rule in summary:
            print(f"  {rule['rule_name']}: {rule['compliance']}")
    else:
        if not args.rule:
            print("❌ --rule required for details")
            exit(1)
        non_compliant = evaluator.get_non_compliant_resources(args.rule)
        print(f"Non-compliant resources for rule {args.rule}:")
        for res in non_compliant:
            print(f"  - {res['resource_type']}/{res['resource_id']}: {res['annotation']}")
