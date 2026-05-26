import boto3
import argparse
import uuid
import time
class S3FargatePipeline:
    def __init__(self, region='us-east-1'):
        self.s3 = boto3.client('s3', region_name=region)
        self.ecs = boto3.client('ecs', region_name=region)
    def upload_file(self, bucket, key, local_path):
        self.s3.upload_file(local_path, bucket, key)
        print(f"Uploaded {local_path} to s3://{bucket}/{key}")
    def run_fargate_task(self, cluster, task_definition, subnets, security_groups, overrides=None):
        response = self.ecs.run_task(
            cluster=cluster,
            taskDefinition=task_definition,
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
        tasks = response['tasks']
        if not tasks:
            print("Failed to start task:", response['failures'])
            return None
        task_arn = tasks[0]['taskArn']
        print(f"Started Fargate task: {task_arn}")
        return task_arn