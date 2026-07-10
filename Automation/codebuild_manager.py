import boto3
import argparse
import time
import sys

class CodeBuildManager:
    def __init__(self, region='us-east-1'):
        self.codebuild = boto3.client('codebuild', region_name=region)