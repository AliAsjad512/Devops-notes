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