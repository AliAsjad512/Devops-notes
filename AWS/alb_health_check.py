import boto3
import argparse

class ALBHealthChecker:
    def __init__(self, target_group_arn, region='us-east-1'):
        self.elbv2 = boto3.client('elbv2', region_name=region)
        self.tg_arn = target_group_arn

    def check_health(self):
        """Get health status of all targets."""
        response = self.elbv2.describe_target_health(TargetGroupArn=self.tg_arn)
        targets = response['TargetHealthDescriptions']
        healthy = 0
        unhealthy = 0

        for target in targets:
            state = target['TargetHealth']['State']
            target_id = target['Target']['Id']
            if state == 'healthy':
                healthy += 1
                print(f"✅ {target_id}: {state}")
            else:
                unhealthy += 1
                reason = target['TargetHealth'].get('Reason', '')
                print(f"❌ {target_id}: {state} ({reason})")
        print(f"\nSummary: {healthy} healthy, {unhealthy} unhealthy")
        return unhealthy == 0