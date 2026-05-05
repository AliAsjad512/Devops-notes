import boto3
import argparse
import datetime
from collections import defaultdict

class EBSSnapshotScheduler:
    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.region = region