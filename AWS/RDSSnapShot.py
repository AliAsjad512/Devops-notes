import boto3
import argparse
import time
import sys

class RDSBackupCopier:
    def __init__(self, source_region, target_region):
        self.source = boto3.client('rds', region_name=source_region)
        self.target = boto3.client('rds', region_name=target_region)
        self.source_region = source_region
        self.target_region = target_region