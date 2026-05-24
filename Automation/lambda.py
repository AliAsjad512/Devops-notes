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