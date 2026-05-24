import boto3
import argparse
import uuid
import time
class S3FargatePipeline:
    def __init__(self, region='us-east-1'):
        self.s3 = boto3.client('s3', region_name=region)
        self.ecs = boto3.client('ecs', region_name=region)