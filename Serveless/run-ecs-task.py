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
    
       def _wait(self, task_arn):
        while True:
            resp = self.ecs.describe_tasks(cluster=self.cluster, tasks=[task_arn])
            status = resp['tasks'][0]['lastStatus']
            print(f"Status: {status}")
            if status in ('STOPPED', 'DEACTIVATING'):
                break
            time.sleep(5)


    if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cluster', required=True)
    parser.add_argument('--task-def', required=True)
    parser.add_argument('--subnets', nargs='+', required=True)
    parser.add_argument('--sg', nargs='+', required=True)
    parser.add_argument('--region', default='us-east-1')
    parser.add_argument('--command', help='Override container command (JSON list, e.g. ["python","script.py"])')
    parser.add_argument('--wait', action='store_true')
    args = parser.parse_args()

    overrides = {}
    if args.command:
        import json
        overrides = {'containerOverrides': [{'name': 'my-container', 'command': json.loads(args.command)}]}
    runner = ECSFargateRunner(args.cluster, args.task_def, args.region)
    runner.run(args.subnets, args.sg, overrides, args.wait)


