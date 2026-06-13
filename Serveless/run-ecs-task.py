import boto3
import argparse
import json
import time

class ECSFargateRunner:
    def __init__(self, cluster, task_definition, region='us-east-1'):
        self.ecs = boto3.client('ecs', region_name=region)
        self.cluster = cluster
        self.task_definition = task_definition


        def run(self, subnets, security_groups, overrides=None, wait=False):
        """Run a Fargate task and optionally wait for completion."""
        response = self.ecs.run_task(
            cluster=self.cluster,
            taskDefinition=self.task_definition,
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': subnets,
                    'securityGroups': security_groups,
                    'assignPublicIp': 'ENABLED'
                }
            },
            overrides=overrides or {}
        )
        if not response['tasks']:
            print(f"Failed: {response['failures']}")
            return None
        task_arn = response['tasks'][0]['taskArn']
        print(f"Started task: {task_arn}")
        if wait:
            self._wait(task_arn)
        return task_arn


