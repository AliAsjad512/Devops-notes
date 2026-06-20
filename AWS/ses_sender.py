import boto3
import argparse
import json

class SESEmailSender:
    def __init__(self, region='us-east-1'):
        self.ses = boto3.client('ses', region_name=region)