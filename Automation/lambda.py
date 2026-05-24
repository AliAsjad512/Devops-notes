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
    def wait_for_task(self, cluster, task_arn, timeout=300):
        start = time.time()
        while time.time() - start < timeout:
            resp = self.ecs.describe_tasks(cluster=cluster, tasks=[task_arn])
            status = resp['tasks'][0]['lastStatus']
            print(f"Task status: {status}")
            if status in ('STOPPED', 'DEACTIVATING'):
                break
            time.sleep(5)
        return status
    def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', required=True)
    parser.add_argument('--key', required=True)
    parser.add_argument('--file', required=True)
    parser.add_argument('--cluster', required=True)
    parser.add_argument('--task-definition', required=True)
    parser.add_argument('--subnets', nargs='+', required=True)
    parser.add_argument('--security-groups', nargs='+', required=True)
    parser.add_argument('--region', default='us-east-1')
    args = parser.parse_args()