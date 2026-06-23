import boto3
import argparse

class ALBHealthChecker:
    def __init__(self, target_group_arn, region='us-east-1'):
        self.elbv2 = boto3.client('elbv2', region_name=region)
        self.tg_arn = target_group_arn