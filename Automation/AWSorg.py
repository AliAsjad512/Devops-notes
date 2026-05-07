import boto3
import argparse
import datetime
import json
from collections import defaultdict

class AWSOrgReport:
    def __init__(self, region='us-east-1'):
        self.org = boto3.client('organizations')
        self.ce = boto3.client('ce', region_name=region)
        self.config = boto3.client('config', region_name=region)
    def list_accounts(self):
        accounts = []
        paginator = self.org.get_paginator('list_accounts')
        for page in paginator.paginate():
            accounts.extend(page['Accounts'])
        return accounts