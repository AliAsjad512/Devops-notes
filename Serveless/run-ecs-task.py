import boto3
import argparse
import json
import time

class ECSFargateRunner:
    def __init__(self, cluster, task_definition, region='us-east-1'):
        self.ecs = boto3.client('ecs', region_name=region)
        self.cluster = cluster
        self.task_definition = task_definition

